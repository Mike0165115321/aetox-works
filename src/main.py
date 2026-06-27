# Aetox Works — Main Entry Point
# เรียกใช้ Supervisor Graph

from src.supervisor.workflow import build_supervisor_graph


def main():
    """รัน Aetox Works Supervisor"""
    
    graph = build_supervisor_graph()
    
    # ตัวอย่างการเรียกใช้
    result = graph.invoke({
        "input": "สร้าง landing page สำหรับโปรโมทสินค้า",
        "plan": "",
        "current_agent": "",
        "messages": [],
        "results": {},
        "final_output": "",
        "error": None,
    })
    
    print(result.get("final_output", "ไม่มีผลลัพธ์"))


if __name__ == "__main__":
    main()
