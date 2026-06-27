# Aetox Works — Supervisor Workflow
# LangGraph Supervisor-Worker Pipeline
# Sales → Research → Content → Dev → Data

import logging
from langgraph.graph import StateGraph, START, END
from src.supervisor import AgentState, AGENT_REGISTRY
from src.llm.client import call_llm

# Agent nodes (real implementations with tools)
from src.agents.sales_agent import sales_node
from src.agents.research_agent import research_node
from src.agents.content_agent import content_node
from src.agents.dev_agent import dev_node
from src.agents.data_agent import data_node

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
log = logging.getLogger("aetox")


def router_llm(state: AgentState) -> str:
    """ใช้ LLM วิเคราะห์ intent และเลือก agent ที่เหมาะสม"""
    user_input = state.get("input", "")
    agent_list = "\n".join(
        [f"- {name}: {desc}" for name, desc in AGENT_REGISTRY.items()]
    )

    prompt = f"""วิเคราะห์คำขอต่อไปนี้ และเลือก agent ที่เหมาะสมที่สุด

คำขอ: "{user_input}"

Agent ที่มี:
{agent_list}

ตอบแค่ชื่อ agent เท่านั้น (คำเดียว) ไม่ต้องอธิบายเพิ่ม"""

    log.info("Router input: %s", user_input)

    try:
        reply = call_llm(prompt, system_prompt="คุณเป็นผู้ช่วยเลือก agent ให้เหมาะสม")
        chosen = reply.strip().lower()

        if chosen in AGENT_REGISTRY:
            log.info("Router -> %s (LLM)", chosen)
            return chosen

        for name in AGENT_REGISTRY:
            if name in chosen or chosen in name:
                log.info("Router -> %s (fuzzy match: %s)", name, chosen)
                return name

        log.warning("Router unknown response: %s — fallback to dev", chosen)
        return "dev"

    except Exception as e:
        log.error("Router error: %s — fallback to dev", e)
        return "dev"


def supervisor_node(state: AgentState) -> AgentState:
    """Supervisor: รับคำสั่ง วางแผน ส่งต่อ"""
    return {
        "plan": f"Supervisor: รับคำสั่ง '{state['input']}'",
        "messages": [("system", f"Supervisor: รับคำสั่ง '{state['input']}'")],
    }


def final_aggregator(state: AgentState) -> AgentState:
    """รวมผลลัพธ์จากทุก agent สรุปส่งผู้ใช้"""
    results = state.get("results", {})
    # ถ้า Data Agent ทำเสร็จแล้ว มี final_output → ใช้เลย
    final = state.get("final_output", "")
    if final:
        return {"final_output": final}

    summary_lines = [f"[{k}] {v[:200]}..." for k, v in results.items()]
    summary = "\n".join(summary_lines)
    log.info("Final output: %d results", len(results))
    return {
        "final_output": f"## Summary\n\n{summary}" if summary else "No results."
    }


def build_supervisor_graph() -> StateGraph:
    """สร้าง Supervisor-Worker Graph พร้อม pipeline agents"""
    graph = StateGraph(AgentState)

    graph.add_node("supervisor", supervisor_node)
    graph.add_node("final", final_aggregator)

    # Agent nodes with real tools
    graph.add_node("sales", sales_node)
    graph.add_node("research", research_node)
    graph.add_node("content", content_node)
    graph.add_node("dev", dev_node)
    graph.add_node("data", data_node)

    graph.add_edge(START, "supervisor")
    graph.add_conditional_edges("supervisor", router_llm, {
        name: name for name in AGENT_REGISTRY
    })

    # Pipeline: เชื่อมแต่ละ agent ต่อกัน
    # สำหรับ Phase 1: single-agent routing (router เลือก agent → final)
    # สำหรับ Phase 2+: จะเปลี่ยนเป็น pipeline sequential
    for name in AGENT_REGISTRY:
        graph.add_edge(name, "final")

    graph.add_edge("final", END)

    return graph.compile()
