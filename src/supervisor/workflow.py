# Aetox Works — Supervisor Workflow
# กำหนด Graph workflow ด้วย LangGraph

from langgraph.graph import StateGraph, START, END
from src.supervisor import AgentState, AGENT_REGISTRY


def router(state: AgentState) -> str:
    """ตัดสินใจว่าให้ agent ไหนทำงานต่อ"""
    # TODO: ใช้ LLM วิเคราะห์ intent แล้วเลือก agent
    # ชั่วคราว: ส่งไป dev agent ก่อน
    return "dev"


def supervisor_node(state: AgentState) -> AgentState:
    """Supervisor: รับคำสั่ง วางแผน ส่งต่อ"""
    # TODO: ใช้ LLM วางแผนการทำงาน
    return {
        "plan": f"วางแผน: {state['input']}",
        "messages": [("system", f"Supervisor: รับคำสั่ง '{state['input']}'")]
    }


def final_aggregator(state: AgentState) -> AgentState:
    """รวมผลลัพธ์จากทุก agent สรุปส่งผู้ใช้"""
    results = state.get("results", {})
    summary = "\n".join([f"[{k}] {v}" for k, v in results.items()])
    return {
        "final_output": f"## สรุปผล\n\n{summary}" if summary else "ไม่มีผลลัพธ์"
    }


def build_supervisor_graph() -> StateGraph:
    """สร้าง Supervisor-Worker Graph"""
    
    graph = StateGraph(AgentState)
    
    # Node
    graph.add_node("supervisor", supervisor_node)
    graph.add_node("final", final_aggregator)
    
    # Edge
    graph.add_edge(START, "supervisor")
    graph.add_conditional_edges("supervisor", router, {
        name: name for name in AGENT_REGISTRY
    })
    
    # Worker agents (placeholder — จะเพิ่มเมื่อสร้าง agent จริง)
    # graph.add_node("sales", sales_agent)
    # graph.add_node("dev", dev_agent)
    # graph.add_node("video", video_agent)
    # graph.add_node("admin", admin_agent)
    
    # รอเชื่อมต่อเมื่อมี agent จริง
    for name in AGENT_REGISTRY:
        graph.add_edge(name, "final")
    
    graph.add_edge("final", END)
    
    return graph.compile()
