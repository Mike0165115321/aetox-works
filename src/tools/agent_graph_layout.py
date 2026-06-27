"""Persistent layout for the Admin agent graph."""
from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any


_LAYOUT_PATH = Path(__file__).parent.parent.parent / "data" / "agent_graph_layout.json"

KNOWN_NODE_IDS = {
    "personal_assistant",
    "sales",
    "research",
    "content",
    "dev",
    "data",
    "final",
}

DEFAULT_LAYOUT: dict[str, dict[str, float]] = {
    "personal_assistant": {"x": 50, "y": 52},
    "sales": {"x": 15, "y": 24},
    "research": {"x": 38, "y": 16},
    "content": {"x": 62, "y": 16},
    "dev": {"x": 85, "y": 24},
    "data": {"x": 78, "y": 80},
    "final": {"x": 22, "y": 80},
}


def get_layout() -> dict[str, Any]:
    """Return saved node positions merged with defaults."""
    saved = _read_saved()
    merged = deepcopy(DEFAULT_LAYOUT)
    for node_id, pos in saved.items():
        if node_id in KNOWN_NODE_IDS:
            merged[node_id] = _sanitize_pos(pos, merged[node_id])
    return {"nodes": merged}


def save_layout(payload: dict[str, Any]) -> dict[str, Any]:
    """Persist known node positions, clamped to the graph viewport."""
    nodes = payload.get("nodes", {}) if isinstance(payload, dict) else {}
    current = get_layout()["nodes"]
    if isinstance(nodes, dict):
        for node_id, pos in nodes.items():
            if node_id in KNOWN_NODE_IDS:
                current[node_id] = _sanitize_pos(pos, current[node_id])

    _LAYOUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    _LAYOUT_PATH.write_text(
        json.dumps({"nodes": current}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return {"nodes": current}


def reset_layout() -> dict[str, Any]:
    """Remove the saved layout and return defaults."""
    if _LAYOUT_PATH.exists():
        _LAYOUT_PATH.unlink()
    return {"nodes": deepcopy(DEFAULT_LAYOUT)}


def _read_saved() -> dict[str, Any]:
    if not _LAYOUT_PATH.exists():
        return {}
    try:
        data = json.loads(_LAYOUT_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}
    nodes = data.get("nodes", {}) if isinstance(data, dict) else {}
    return nodes if isinstance(nodes, dict) else {}


def _sanitize_pos(pos: Any, fallback: dict[str, float]) -> dict[str, float]:
    if not isinstance(pos, dict):
        return dict(fallback)
    return {
        "x": _clamp(pos.get("x", fallback["x"])),
        "y": _clamp(pos.get("y", fallback["y"])),
    }


def _clamp(value: Any) -> float:
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        numeric = 50.0
    return max(5.0, min(95.0, numeric))
