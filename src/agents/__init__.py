# Aetox Works — Agent Base
# template สำหรับสร้าง worker agent ใหม่

from typing import Any
from src.supervisor import AgentState


class BaseAgent:
    """Base class สำหรับ worker agent ทั้งหมด"""
    
    name: str = ""
    description: str = ""
    
    def __call__(self, state: AgentState) -> dict:
        """Execute agent logic"""
        raise NotImplementedError
    
    @property
    def node_name(self) -> str:
        """ชื่อ node ใน LangGraph"""
        return self.name
