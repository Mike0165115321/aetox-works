# Video Agent — ตัดต่อวิดีโอ, TTS, คำบรรยาย

from src.agents import BaseAgent
from src.supervisor import AgentState


class VideoAgent(BaseAgent):
    name = "video"
    description = "Video Agent — ตัดต่อวิดีโอ, ใส่ TTS, คำบรรยาย"
    
    def __call__(self, state: AgentState) -> dict:
        # TODO: integrate with HyperFrames
        return {
            "results": {"video": "Video agent ทำงานเสร็จ"},
            "messages": [("system", "Video Agent: เสร็จแล้ว")]
        }


video_agent = VideoAgent()
