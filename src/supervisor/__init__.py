# Aetox Works — Supervisor Agent
# Supervisor ทำหน้าที่รับคำสั่ง วางแผน และส่งต่องานให้ worker agents
# ใช้ LangGraph Supervisor-Worker Pattern

from typing import Annotated, Literal, TypedDict
import operator


class AgentState(TypedDict):
    """สถานะของระบบ — ใช้ shared state ทั่วทั้ง graph"""
    input: str                          # คำสั่งเริ่มต้นจากผู้ใช้
    plan: str                           # แผนการทำงาน
    current_agent: str                  # agent ที่กำลังทำงาน
    messages: Annotated[list, operator.add]  # ประวัติการสนทนา
    results: dict                       # ผลลัพธ์จากแต่ละ agent
    final_output: str                   # ผลลัพธ์final
    error: str | None                   # ข้อผิดพลาด


# Agent types ที่ระบบรองรับ
# เพิ่ม agent ใหม่ → แค่เติมใน AGENT_REGISTRY และสร้างไฟล์ใน src/agents/
AGENT_REGISTRY = {
    "sales":    "Sales Agent — เก็บโจทย์ลูกค้า, pain point, สรุป需求",
    "research": "Research Agent — หาข้อมูลตลาด, คู่แข่ง, keyword, insight",
    "content":  "Content Agent — เขียน copy, landing content, article",
    "dev":      "Dev Agent — สร้างเว็บ, feature, automation",
    "data":     "Data Agent — วิเคราะห์ผลลัพธ์ lead/content/performance",
}

# เพิ่ม agent ใหม่ → แค่เติมใน AGENT_REGISTRY และสร้างไฟล์ใน src/agents/
