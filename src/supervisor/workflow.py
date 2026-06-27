# Aetox Works — Supervisor Workflow
# LangGraph Supervisor-Worker pattern

import logging
from langgraph.graph import StateGraph, START, END
from src.supervisor import AgentState, AGENT_REGISTRY
from src.llm.client import call_llm
from src.config.agent_configs import get_system_prompt

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

        # ตรวจสอบว่า LLM ตอบชื่อ agent ที่มีอยู่จริง
        if chosen in AGENT_REGISTRY:
            log.info("Router -> %s (LLM)", chosen)
            return chosen

        # ถ้าตอบไม่ตรงชื่อ — ลองจับคู่บางส่วน
        for name in AGENT_REGISTRY:
            if name in chosen or chosen in name:
                log.info("Router -> %s (fuzzy match: %s)", name, chosen)
                return name

        # ไม่ match เลย
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
    """รวมผลลัพธ์จาก agent สรุปส่งผู้ใช้"""
    results = state.get("results", {})
    summary_lines = [f"[{k}] {v}" for k, v in results.items()]
    summary = "\n".join(summary_lines)

    log.info("Final output: %d results", len(results))

    return {
        "final_output": f"## Summary\n\n{summary}" if summary else "No results."
    }


def make_agent(name: str, desc: str):
    """สร้าง agent node — ใช้ prompt จาก agent_configs"""
    prompt = get_system_prompt(name)
    if not prompt:
        prompt = f"คุณคือ {name} Agent: {desc}"

    def agent_node(state: AgentState) -> dict:
        user_input = state.get("input", "")
        log.info("Agent %s received: %s", name, user_input[:80])

        # ถ้ามี prompt จริง → เรียก LLM ด้วย system prompt
        try:
            reply = call_llm(
                f"คำขอ: {user_input}\n\nตอบกลับเป็นสรุปผลงานของคุณ",
                system_prompt=prompt,
            )
            log.info("Agent %s responded (%d chars)", name, len(reply))
            return {
                "results": {name: reply},
                "messages": [("system", f"{name}: {reply}")],
            }
        except Exception as e:
            log.warning("Agent %s LLM error: %s — fallback", name, e)
            return {
                "results": {name: f"[{name}] {desc}"},
                "messages": [("system", f"{name}: LLM error — {e}")],
            }

    agent_node.__name__ = name
    return agent_node


def build_supervisor_graph() -> StateGraph:
    """สร้าง Supervisor-Worker Graph"""
    graph = StateGraph(AgentState)

    graph.add_node("supervisor", supervisor_node)
    graph.add_node("final", final_aggregator)

    for name, desc in AGENT_REGISTRY.items():
        graph.add_node(name, make_agent(name, desc))

    graph.add_edge(START, "supervisor")
    graph.add_conditional_edges("supervisor", router_llm, {
        name: name for name in AGENT_REGISTRY
    })

    for name in AGENT_REGISTRY:
        graph.add_edge(name, "final")

    graph.add_edge("final", END)

    return graph.compile()
