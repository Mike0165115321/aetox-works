# Aetox Works — Supervisor Workflow
# LangGraph Supervisor-Worker Pipeline
# Sales → Research → Content → Dev → Data
#
# Modes:
#   pipeline (default) — sequential: วิ่งผ่านทุก agent ตามลำดับ
#   router — single-agent: เลือก agent เดียวตาม intent

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

# Pipeline order — ลำดับการทำงานแบบ sequential
PIPELINE_ORDER = ["sales", "research", "content", "dev", "data"]


def router_llm(state: AgentState) -> str:
    """ใช้ LLM วิเคราะห์ intent และเลือก agent ที่เหมาะสม (router mode)"""
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
    # Keep conversation_context if passed from chat
    ctx = state.get("conversation_context", "")
    return {
        "plan": f"Supervisor: รับคำสั่ง '{state['input']}'",
        "messages": [("system", f"Supervisor: รับคำสั่ง '{state['input']}'")],
        "conversation_context": ctx,
        "sales_notebook": state.get("sales_notebook", {}),
        "handoff_brief": state.get("handoff_brief", {}),
    }


def final_aggregator(state: AgentState) -> AgentState:
    """รวมผลลัพธ์จากทุก agent สรุปส่งผู้ใช้"""
    final = state.get("final_output", "")
    ctx = state.get("conversation_context", "")
    if final:
        return {"final_output": final, "conversation_context": ctx}

    results = state.get("results", {})
    agent_names = [k for k in results.keys()]
    summary_lines = [f"- [{k}] complete" for k in agent_names]
    summary = "\n".join(summary_lines)
    log.info("Final output: %d results from %s", len(results), agent_names)
    return {
        "final_output": f"## Pipeline Complete\n\n{summary}" if summary else "No results.",
        "conversation_context": ctx,
    }


def pipeline_next_agent(state: AgentState) -> str:
    """
    Pipeline router: sales → research → content → dev → data → final

    ⚠️ CRITICAL: Sales ต้อง confirmed ก่อนถึงจะไปต่อ
    ถ้าข้อมูลยังไม่ครบ → หยุดรอ (ไม่ loop)
    """
    results = state.get("results", {})
    sales_done = "sales" in results
    sales_confirmed = state.get("sales_confirmed", False)
    notebook = state.get("sales_notebook") or {}

    # Sales has run already (results, notebook, or conversation exists)
    sales_has_run = sales_done or bool(notebook) or bool(state.get("conversation_context"))

    # If sales ran but not confirmed → STOP (don't loop back to sales)
    if sales_has_run and not sales_confirmed:
        log.info("Pipeline: sales active (notebook=%s) → final (awaiting confirmation)", 
                 notebook.get("_nb_id", "?"))
        return "final"

    # If sales confirmed but somehow not in results yet (edge case)
    if sales_confirmed and not sales_done:
        return "sales"  # re-run sales to get the confirmation output

    # Find last completed agent
    for agent_name in reversed(PIPELINE_ORDER):
        if agent_name in results:
            idx = PIPELINE_ORDER.index(agent_name)
            if idx + 1 < len(PIPELINE_ORDER):
                next_agent = PIPELINE_ORDER[idx + 1]
                log.info("Pipeline: %s → %s", agent_name, next_agent)
                return next_agent
            else:
                log.info("Pipeline: complete → final")
                return "final"
            break

    # No agent has run yet → start at sales
    log.info("Pipeline: start → sales")
    return "sales"


def build_pipeline_graph() -> StateGraph:
    """
    Pipeline Mode — Sequential: Sales → Research → Content → Dev → Data

    ใช้สำหรับ production workflow ที่ต้องการทำทุกขั้นตอน
    """
    graph = StateGraph(AgentState)

    graph.add_node("supervisor", supervisor_node)
    graph.add_node("final", final_aggregator)

    # Agent nodes
    graph.add_node("sales", sales_node)
    graph.add_node("research", research_node)
    graph.add_node("content", content_node)
    graph.add_node("dev", dev_node)
    graph.add_node("data", data_node)

    # Start → supervisor → pipeline routing
    graph.add_edge(START, "supervisor")
    graph.add_conditional_edges("supervisor", pipeline_next_agent, {
        "sales": "sales",
        "research": "research",
        "content": "content",
        "dev": "dev",
        "data": "data",
        "final": "final",
    })

    # Pipeline chain: each agent → next in sequence
    graph.add_conditional_edges("sales", pipeline_next_agent, {
        "research": "research",
        "content": "content",
        "dev": "dev",
        "data": "data",
        "final": "final",
    })
    graph.add_conditional_edges("research", pipeline_next_agent, {
        "content": "content",
        "dev": "dev",
        "data": "data",
        "final": "final",
    })
    graph.add_conditional_edges("content", pipeline_next_agent, {
        "dev": "dev",
        "data": "data",
        "final": "final",
    })
    graph.add_conditional_edges("dev", pipeline_next_agent, {
        "data": "data",
        "final": "final",
    })
    graph.add_conditional_edges("data", pipeline_next_agent, {
        "final": "final",
    })

    graph.add_edge("final", END)

    return graph.compile()


def build_router_graph() -> StateGraph:
    """
    Router Mode — Single Agent: เลือก agent เดียวตาม intent

    ใช้สำหรับ quick tasks ที่ต้องการ agent เดียว
    """
    graph = StateGraph(AgentState)

    graph.add_node("supervisor", supervisor_node)
    graph.add_node("final", final_aggregator)

    # Agent nodes
    graph.add_node("sales", sales_node)
    graph.add_node("research", research_node)
    graph.add_node("content", content_node)
    graph.add_node("dev", dev_node)
    graph.add_node("data", data_node)

    graph.add_edge(START, "supervisor")
    graph.add_conditional_edges("supervisor", router_llm, {
        name: name for name in AGENT_REGISTRY
    })

    # Single agent → final
    for name in AGENT_REGISTRY:
        graph.add_edge(name, "final")

    graph.add_edge("final", END)

    return graph.compile()


def build_supervisor_graph(mode: str = "pipeline") -> StateGraph:
    """
    สร้าง Supervisor-Worker Graph

    Args:
        mode: "pipeline" (sequential, default) หรือ "router" (single-agent)

    Returns:
        compiled StateGraph
    """
    if mode == "router":
        log.info("Building graph: ROUTER mode (single-agent)")
        return build_router_graph()

    log.info("Building graph: PIPELINE mode (sequential)")
    return build_pipeline_graph()
