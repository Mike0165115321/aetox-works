"""
Aetox Works — FastAPI Server 🚀
Phase 7: Production API with Authentication, Logging, Pipeline/Agent Endpoints

Run: python -m src.api.server
"""
import os
import time
import uuid
import logging
from datetime import datetime, timezone
from typing import Any

from fastapi import FastAPI, Request, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel, Field
import uvicorn

from src.supervisor.workflow import build_supervisor_graph
from src.tools.crm import list_leads
from src.tools.content_store import list_drafts
from src.tools.builder import list_projects
from src.tools.reporter import aggregate_metrics

# ═══════════════════════════════════════════════════════════
# Logging Setup
# ═══════════════════════════════════════════════════════════

log = logging.getLogger("aetox.api")
log.setLevel(logging.INFO)

# File handler สำหรับ request log
_log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
os.makedirs(_log_dir, exist_ok=True)
_fh = logging.FileHandler(os.path.join(_log_dir, "api.log"), encoding="utf-8")
_fh.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
log.addHandler(_fh)


# ═══════════════════════════════════════════════════════════
# Authentication
# ═══════════════════════════════════════════════════════════

AETOX_API_KEY = os.getenv("AETOX_API_KEY", "")


def verify_api_key(x_api_key: str | None = None) -> None:
    """
    ตรวจสอบ API key จาก header X-API-Key

    ถ้าไม่ได้ตั้ง AETOX_API_KEY ใน .env → bypass (dev mode)
    """
    if not AETOX_API_KEY:
        # Dev mode — no auth required
        return

    if not x_api_key:
        raise HTTPException(status_code=401, detail="Missing X-API-Key header")

    # Constant-time comparison ป้องกัน timing attack
    if not _secure_compare(x_api_key, AETOX_API_KEY):
        raise HTTPException(status_code=403, detail="Invalid API key")


def _secure_compare(a: str, b: str) -> bool:
    """Constant-time string comparison"""
    if len(a) != len(b):
        return False
    result = 0
    for x, y in zip(a, b):
        result |= ord(x) ^ ord(y)
    return result == 0


# ═══════════════════════════════════════════════════════════
# Pydantic Schemas
# ═══════════════════════════════════════════════════════════

class PipelineRequest(BaseModel):
    input: str = Field(..., min_length=1, max_length=5000, description="คำสั่ง/ความต้องการ")
    mode: str = Field(default="pipeline", pattern="^(pipeline|router)$")


class PipelineResponse(BaseModel):
    request_id: str
    mode: str
    input: str
    output: str
    agents_used: list[str]
    elapsed_ms: int
    status: str


class HealthResponse(BaseModel):
    status: str = "ok"
    version: str = "1.0.0"
    timestamp: str


class StatusResponse(BaseModel):
    leads_count: int
    drafts_count: int
    projects_count: int
    metrics: dict[str, float]
    uptime_seconds: float


# ═══════════════════════════════════════════════════════════
# FastAPI App
# ═══════════════════════════════════════════════════════════

app = FastAPI(
    title="Aetox Works API",
    description="AI Enterprise Workforce — LangGraph Supervisor-Worker Pipeline",
    version="1.0.0",
)

# CORS — เปิดให้ local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup time
_start_time = time.time()


# ═══════════════════════════════════════════════════════════
# Middleware — Request Tracing
# ═══════════════════════════════════════════════════════════

@app.middleware("http")
async def trace_requests(request: Request, call_next):
    """Log ทุก request พร้อม request_id และ timing"""
    req_id = str(uuid.uuid4())[:8]
    start = time.time()

    # Attach request_id to request state
    request.state.request_id = req_id

    log.info("[%s] %s %s", req_id, request.method, request.url.path)

    response = await call_next(request)

    elapsed = (time.time() - start) * 1000
    log.info("[%s] %d %s — %.0fms", req_id, response.status_code, request.url.path, elapsed)

    response.headers["X-Request-ID"] = req_id
    return response


# ═══════════════════════════════════════════════════════════
# Routes
# ═══════════════════════════════════════════════════════════

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    """🎛️ Unified Dashboard — ภาพรวมระบบ + Chat + Leads + Content + Projects"""
    from src.api.dashboard import DASHBOARD_HTML
    return DASHBOARD_HTML


@app.get("/chat", response_class=HTMLResponse)
async def chat_page():
    """💬 Aetox Chat — Multi-Agent Pipeline Showcase"""
    from src.api.chat_ui import CHAT_HTML
    return CHAT_HTML


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="ok",
        version="1.0.0",
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


@app.get("/status", response_model=StatusResponse)
async def system_status():
    """สถานะระบบ — leads, drafts, projects, metrics"""
    try:
        leads = len(list_leads(limit=1000))
    except Exception:
        leads = -1

    try:
        drafts = len(list_drafts(limit=1000))
    except Exception:
        drafts = -1

    try:
        projects = len(list_projects())
    except Exception:
        projects = -1

    try:
        metrics = aggregate_metrics()
    except Exception:
        metrics = {}

    return StatusResponse(
        leads_count=leads,
        drafts_count=drafts,
        projects_count=projects,
        metrics=metrics,
        uptime_seconds=round(time.time() - _start_time, 1),
    )


@app.post("/pipeline/run", response_model=PipelineResponse)
async def run_pipeline(
    req: PipelineRequest,
    x_api_key: str | None = None,
):
    """
    🚀 รัน Aetox Pipeline — วิ่งผ่านทุก agent ตามลำดับ

    **Pipeline mode:** Sales → Research → Content → Dev → Data
    **Router mode:** เลือก agent เดียวตาม intent
    """
    verify_api_key(x_api_key)

    req_id = str(uuid.uuid4())[:8]
    start = time.time()

    log.info("[%s] Pipeline start — mode=%s input=%s", req_id, req.mode, req.input[:80])

    try:
        graph = build_supervisor_graph(mode=req.mode)
        result = graph.invoke({
            "input": req.input,
            "plan": "",
            "current_agent": "",
            "messages": [],
            "results": {},
            "final_output": "",
            "error": None,
        })

        agents_used = [k for k in result.get("results", {})]
        output = result.get("final_output", "No output")

        elapsed_ms = int((time.time() - start) * 1000)
        log.info("[%s] Pipeline done — %d agents, %dms", req_id, len(agents_used), elapsed_ms)

        return PipelineResponse(
            request_id=req_id,
            mode=req.mode,
            input=req.input[:200],
            output=output,
            agents_used=agents_used,
            elapsed_ms=elapsed_ms,
            status="success",
        )

    except Exception as e:
        elapsed_ms = int((time.time() - start) * 1000)
        log.error("[%s] Pipeline error: %s", req_id, e)
        raise HTTPException(status_code=500, detail=f"Pipeline error: {str(e)}")


@app.post("/agent/run")
async def run_single_agent(
    req: PipelineRequest,
    x_api_key: str | None = None,
):
    """
    🎯 รัน Agent เดียว (alias ของ /pipeline/run?mode=router)
    """
    verify_api_key(x_api_key)
    req.mode = "router"
    return await run_pipeline(req, x_api_key)


# ═══════════════════════════════════════════════════════════
# Dashboard Data APIs
# ═══════════════════════════════════════════════════════════

@app.get("/api/leads")
async def api_leads(status: str | None = Query(None), limit: int = Query(50, le=200)):
    """👥 ดึงรายการ leads พร้อมกรองตาม status"""
    try:
        from src.tools.crm import list_leads
        leads = list_leads(status=status, limit=limit)
        return {"success": True, "data": leads, "count": len(leads)}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.get("/api/leads/{lead_id}")
async def api_lead_detail(lead_id: int):
    """👤 ดึงข้อมูล lead แบบละเอียด"""
    try:
        from src.tools.crm import get_lead
        lead = get_lead(lead_id)
        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")
        return {"success": True, "data": lead}
    except HTTPException:
        raise
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.put("/api/leads/{lead_id}/status")
async def api_lead_status(lead_id: int, status: str = Query(...)):
    """🔄 อัปเดตสถานะ lead"""
    try:
        from src.tools.crm import update_lead_status
        ok = update_lead_status(lead_id, status)
        return {"success": ok}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.get("/api/drafts")
async def api_drafts(content_type: str | None = Query(None), limit: int = Query(50, le=200)):
    """✍️ ดึงรายการ content drafts"""
    try:
        from src.tools.content_store import list_drafts
        drafts = list_drafts(content_type=content_type, limit=limit)
        return {"success": True, "data": drafts, "count": len(drafts)}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.get("/api/reports")
async def api_reports(limit: int = Query(20, le=100)):
    """📊 ดึงรายการ reports"""
    try:
        from src.tools.reporter import list_reports
        reports = list_reports(limit=limit)
        return {"success": True, "data": reports, "count": len(reports)}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.get("/api/projects")
async def api_projects():
    """🌐 ดึงรายการโปรเจคที่ Dev Agent สร้าง"""
    try:
        from src.tools.builder import list_projects
        projects = list_projects()
        return {"success": True, "data": projects, "count": len(projects)}
    except Exception as e:
        return {"success": False, "error": str(e)}


# ═══════════════════════════════════════════════════════════
# Entry Point
# ═══════════════════════════════════════════════════════════

def main():
    """Run API server"""
    host = os.getenv("AETOX_HOST", "127.0.0.1")
    port = int(os.getenv("AETOX_PORT", "8000"))

    auth_status = "DEV MODE (no auth)" if not AETOX_API_KEY else "AUTH ENABLED"
    print(f"""
+==========================================+
|        Aetox Works API v1.0              |
+==========================================+
|  {auth_status:<36} |
|  API:     http://{host}:{port:<5}              |
|  Docs:    http://{host}:{port}/docs           |
|  Dashboard: http://{host}:{port}/             |
+==========================================+
""")

    uvicorn.run(
        "src.api.server:app",
        host=host,
        port=port,
        reload=False,
        log_level="info",
    )


if __name__ == "__main__":
    main()
