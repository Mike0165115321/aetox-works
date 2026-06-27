# Sales Agent — ติดต่อลูกค้า สรุปความต้องการ

from src.agents import BaseAgent
from src.supervisor import AgentState


class SalesAgent(BaseAgent):
    name = "sales"
    description = "Sales Agent — ติดต่อลูกค้า สรุปความต้องการ"
    
    def __call__(self, state: AgentState) -> dict:
        # TODO: implement actual sales workflow
        return {
            "results": {"sales": "Sales agent ทำงานเสร็จ"},
            "messages": [("system", "Sales Agent: เสร็จแล้ว")]
        }


sales_agent = SalesAgent()
