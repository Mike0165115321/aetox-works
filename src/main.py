# Aetox Works — Main Entry Point
# เรียกใช้ Supervisor Graph
# Mode: "pipeline" (sequential) หรือ "router" (single-agent)

from src.supervisor.workflow import build_supervisor_graph


def main(mode: str = "pipeline"):
    """รัน Aetox Works Supervisor"""
    
    graph = build_supervisor_graph(mode=mode)
    
    # ตัวอย่างการเรียกใช้
    result = graph.invoke({
        "input": "สร้าง landing page สำหรับโปรโมทสินค้า AI",
        "plan": "",
        "current_agent": "",
        "messages": [],
        "results": {},
        "final_output": "",
        "error": None,
        "sales_confirmed": False,
        "conversation_context": "",
        "sales_notebook": {},
        "handoff_brief": {},
    })
    
    print("=" * 60)
    print("  Aetox Works — Pipeline Result")
    print("=" * 60)
    print()
    print(result.get("final_output", "ไม่มีผลลัพธ์"))
    print()
    
    # Show agent results summary
    results = result.get("results", {})
    for agent_name in ["sales", "research", "content", "dev", "data"]:
        if agent_name in results:
            print(f"  ✅ {agent_name} — done")
    
    print()
    return result


if __name__ == "__main__":
    main()
