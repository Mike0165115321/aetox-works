"""Runtime status for the currently running agent graph."""
from __future__ import annotations

import json
from copy import deepcopy
from datetime import datetime, timezone
from threading import RLock
from typing import Any

from src.supervisor import AGENT_REGISTRY


ASSISTANT_NODE = "personal_assistant"
FINAL_NODE = "final"
AGENT_ORDER = ["sales", "research", "content", "dev", "data"]
GRAPH_NODE_ORDER = [ASSISTANT_NODE, *AGENT_ORDER, FINAL_NODE]

_lock = RLock()
_state: dict[str, Any] = {}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _node(
    node_id: str,
    name: str,
    role: str,
    note: str = "ยังไม่มีงานในรอบนี้",
) -> dict[str, Any]:
    return {
        "id": node_id,
        "name": name,
        "role": role,
        "state": "idle",
        "label": "Idle",
        "note": note,
        "started_at": None,
        "finished_at": None,
        "error": None,
        "output_summary": "",
    }


def _base_nodes() -> dict[str, dict[str, Any]]:
    nodes = {
        ASSISTANT_NODE: _node(
            ASSISTANT_NODE,
            "Personal Assistant",
            "รับคำสั่ง วางแผน เลือก flow และส่ง shared state/handoff ให้ agent ที่เกี่ยวข้อง",
            "รอคำสั่งจากผู้ใช้",
        ),
        FINAL_NODE: _node(
            FINAL_NODE,
            "Final Output",
            "รวบรวมผลจาก graph แล้วส่งคำตอบสุดท้ายกลับให้ผู้ใช้",
            "รอผลลัพธ์จาก Personal Assistant",
        ),
    }
    for name in AGENT_ORDER:
        nodes[name] = _node(name, name.title(), AGENT_REGISTRY.get(name, ""))
    return nodes


def _base_edges(mode: str = "pipeline", selected_agent: str | None = None) -> list[dict[str, Any]]:
    if mode == "router":
        agents = [selected_agent] if selected_agent in AGENT_ORDER else AGENT_ORDER
        edges = []
        for agent in agents:
            edges.append(_edge(ASSISTANT_NODE, agent, f"route-{agent}", "route"))
            edges.append(_edge(agent, ASSISTANT_NODE, f"return-{agent}", "handoff"))
        edges.append(_edge(ASSISTANT_NODE, FINAL_NODE, "route-final", "final"))
        return edges

    edges = []
    for agent in AGENT_ORDER:
        edges.append(_edge(ASSISTANT_NODE, agent, f"route-{agent}", "route"))
        edges.append(_edge(agent, ASSISTANT_NODE, f"return-{agent}", "handoff"))
    edges.append(_edge(ASSISTANT_NODE, FINAL_NODE, "route-final", "final"))
    return edges


def _edge(source: str, target: str, edge_id: str, kind: str) -> dict[str, Any]:
    return {
        "id": edge_id,
        "from": source,
        "to": target,
        "kind": kind,
        "state": "idle",
    }


def reset_run(run_id: str, mode: str, user_input: str) -> None:
    active_mode = mode if mode in {"pipeline", "router"} else "pipeline"
    now = _now()
    with _lock:
        _state.clear()
        _state.update({
            "run_id": run_id,
            "mode": active_mode,
            "input": user_input[:200],
            "running": True,
            "current_agent": None,
            "selected_agent": None,
            "started_at": now,
            "updated_at": now,
            "finished_at": None,
            "nodes": _base_nodes(),
            "edges": _base_edges(active_mode),
        })
        assistant = _state["nodes"][ASSISTANT_NODE]
        assistant.update({
            "state": "active",
            "label": "Routing",
            "note": "รับคำสั่งและเตรียมเลือก flow",
            "started_at": now,
        })


def mark_agent_running(agent_name: str) -> None:
    with _lock:
        _ensure_state()
        _state["running"] = True
        _state["current_agent"] = agent_name
        _state["selected_agent"] = agent_name
        _state["updated_at"] = _now()
        if _state.get("mode") == "router":
            _state["edges"] = _base_edges("router", agent_name)

        assistant = _state["nodes"][ASSISTANT_NODE]
        assistant.update({
            "state": "done",
            "label": "Routed",
            "note": f"ส่งงานให้ {agent_name.title()} ผ่าน shared state",
            "finished_at": _now(),
            "error": None,
        })

        node = _state["nodes"][agent_name]
        node.update({
            "state": "active",
            "label": "Working",
            "note": "กำลังทำงานจริงใน graph",
            "started_at": node.get("started_at") or _now(),
            "finished_at": None,
            "error": None,
        })

        _set_edge_state(ASSISTANT_NODE, agent_name, "active")


def mark_agent_done(agent_name: str, result: dict[str, Any] | None = None) -> None:
    with _lock:
        _ensure_state()
        result = result or {}
        state = "done"
        label = "Done"
        note = "ทำงานเสร็จแล้ว"
        output_summary = _summarize_agent_result(agent_name, result)

        if agent_name == "sales" and not result.get("sales_confirmed", False):
            state = "waiting"
            label = "Waiting"
            note = "Sales จดข้อมูลแล้ว รอลูกค้ายืนยันก่อนส่งต่อ"
        elif result.get("results", {}).get(agent_name):
            note = "ส่งผลลัพธ์ให้ node ถัดไปแล้ว"

        node = _state["nodes"][agent_name]
        node.update({
            "state": state,
            "label": label,
            "note": note,
            "finished_at": _now(),
            "error": None,
            "output_summary": output_summary,
        })

        _set_edge_state(ASSISTANT_NODE, agent_name, "done" if state == "done" else "waiting")
        _set_edge_state(agent_name, ASSISTANT_NODE, "done" if state == "done" else "waiting")

        idx = AGENT_ORDER.index(agent_name)
        if idx < len(AGENT_ORDER) - 1:
            if state == "done" and _state["nodes"][AGENT_ORDER[idx + 1]]["state"] == "idle":
                _state["nodes"][AGENT_ORDER[idx + 1]].update({
                    "state": "waiting",
                    "label": "Waiting",
                    "note": "รอ Personal Assistant ส่ง state/handoff มาให้",
                })
                _set_edge_state(ASSISTANT_NODE, AGENT_ORDER[idx + 1], "waiting")

        assistant = _state["nodes"][ASSISTANT_NODE]
        assistant.update({
            "state": "waiting" if state == "waiting" else "done",
            "label": "Waiting" if state == "waiting" else "Received",
            "note": "รอลูกค้ายืนยันก่อนส่งต่อ" if state == "waiting" else f"รับผลจาก {agent_name.title()} แล้ว",
            "error": None,
        })

        _state["current_agent"] = None
        _state["updated_at"] = _now()


def mark_agent_error(agent_name: str, error: Exception) -> None:
    with _lock:
        _ensure_state()
        node = _state["nodes"][agent_name]
        node.update({
            "state": "error",
            "label": "Error",
            "note": str(error)[:200],
            "finished_at": _now(),
            "error": str(error),
        })
        _set_edge_state(ASSISTANT_NODE, agent_name, "error")
        _set_edge_state(agent_name, ASSISTANT_NODE, "error")
        _state["nodes"][ASSISTANT_NODE].update({
            "state": "error",
            "label": "Error",
            "note": f"{agent_name.title()} error",
            "error": str(error),
        })
        _state["running"] = False
        _state["current_agent"] = None
        _state["updated_at"] = _now()
        _state["finished_at"] = _now()


def finish_run() -> None:
    with _lock:
        _ensure_state()
        now = _now()
        _state["running"] = False
        _state["current_agent"] = None
        _state["updated_at"] = now
        _state["finished_at"] = now
        if _state["nodes"][ASSISTANT_NODE]["state"] != "error":
            _state["nodes"][ASSISTANT_NODE].update({
                "state": "done",
                "label": "Done",
                "note": "ส่งต่อผลลัพธ์ไป Final Output แล้ว",
                "finished_at": now,
            })
        _state["nodes"][FINAL_NODE].update({
            "state": "done",
            "label": "Done",
            "note": "ตอบกลับผู้ใช้แล้ว",
            "started_at": _state["nodes"][FINAL_NODE].get("started_at") or now,
            "finished_at": now,
        })
        _set_edge_state(ASSISTANT_NODE, FINAL_NODE, "done")


def snapshot() -> dict[str, Any]:
    with _lock:
        _ensure_state()
        data = deepcopy(_state)
        data["nodes"] = [data["nodes"][name] for name in GRAPH_NODE_ORDER]
        return data


def _ensure_state() -> None:
    if _state:
        return
    reset_run("", "pipeline", "")
    _state["running"] = False
    _state["nodes"][ASSISTANT_NODE].update({
        "state": "idle",
        "label": "Idle",
        "note": "รอคำสั่งจากผู้ใช้",
        "started_at": None,
    })


def _set_edge_state(source: str, target: str, state: str) -> None:
    for edge in _state["edges"]:
        if edge["from"] == source and edge["to"] == target:
            edge["state"] = state
            return


def _summarize_agent_result(agent_name: str, result: dict[str, Any]) -> str:
    raw = result.get("results", {}).get(agent_name)
    if not raw:
        return ""
    try:
        data = json.loads(raw) if isinstance(raw, str) else raw
    except (json.JSONDecodeError, TypeError):
        return str(raw)[:220]

    if agent_name == "sales":
        lead_id = data.get("lead_id", "")
        status = data.get("status", "")
        return f"Lead #{lead_id} {status}".strip()
    if agent_name == "research":
        return f"Sources: {data.get('sources', 0)}"
    if agent_name == "content":
        return data.get("title", "")[:220]
    if agent_name == "dev":
        files = data.get("files_built", [])
        return f"{len(files)} files built"
    if agent_name == "data":
        return data.get("summary", data.get("overall_status", ""))[:220]
    return str(data)[:220]
