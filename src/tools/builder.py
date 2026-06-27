"""
Aetox Works — Builder Tools (Dev Agent 💻)

สร้าง HTML, จัดการไฟล์, preview server
"""
import os
import logging
import http.server
import socketserver
import threading
from pathlib import Path
from datetime import datetime
from typing import Any

log = logging.getLogger("aetox.builder")

# output directory สำหรับเว็บที่สร้าง
_OUTPUT_DIR = Path(__file__).parent.parent.parent / "output" / "websites"


def _ensure_output_dir(subdir: str = "") -> Path:
    dir_path = _OUTPUT_DIR / subdir if subdir else _OUTPUT_DIR
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


# ── HTML Templates ────────────────────────────────────────

_LANDING_TEMPLATE = """<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, 'Noto Sans Thai', sans-serif;
         line-height: 1.6; color: #1a1a2e; }}
  .hero {{ background: {hero_bg}; color: {hero_text}; padding: 80px 24px;
           text-align: center; }}
  .hero h1 {{ font-size: 2.5em; margin-bottom: 16px; }}
  .hero p {{ font-size: 1.1em; opacity: 0.9; max-width: 640px; margin: 0 auto 32px; }}
  .cta-btn {{ display: inline-block; padding: 14px 36px; background: {cta_bg};
             color: {cta_text_color}; text-decoration: none; border-radius: 8px;
             font-size: 1.1em; font-weight: 600; }}
  .section {{ max-width: 960px; margin: 0 auto; padding: 60px 24px; }}
  .section h2 {{ text-align: center; font-size: 1.8em; margin-bottom: 40px; }}
  .features {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
              gap: 24px; }}
  .feature {{ background: #f5f5f7; padding: 24px; border-radius: 12px; }}
  .feature h3 {{ margin-bottom: 8px; }}
  .footer {{ text-align: center; padding: 40px 24px; color: #666; font-size: 0.9em; }}
</style>
</head>
<body>
  <section class="hero">
    <h1>{headline}</h1>
    <p>{subheadline}</p>
    <a class="cta-btn" href="{cta_link}">{cta_text}</a>
  </section>
  <section class="section">
    <h2>{features_title}</h2>
    <div class="features">
      {features_html}
    </div>
  </section>
  <div class="footer">
    <p>© {year} Aetox Works — สร้างโดย Dev Agent</p>
  </div>
</body>
</html>"""


def _render_features(features: list[dict[str, str]]) -> str:
    """render feature cards HTML"""
    cards = []
    for f in features:
        cards.append(
            f'<div class="feature"><h3>{f.get("title", "")}</h3>'
            f'<p>{f.get("desc", "")}</p></div>'
        )
    return "\n".join(cards)


def generate_landing(
    title: str = "Landing Page",
    headline: str = "หัวข้อหลัก",
    subheadline: str = "คำอธิบายสั้น ๆ",
    features: list[dict[str, str]] | None = None,
    cta_text: str = "เริ่มต้นเลย",
    cta_link: str = "#",
    hero_bg: str = "#1a1a2e",
    hero_text: str = "#ffffff",
    cta_bg: str = "#e94560",
    cta_text_color: str = "#ffffff",
    features_title: str = "ฟีเจอร์ของเรา",
    output_subdir: str = "",
) -> dict[str, Any]:
    """
    สร้าง Landing Page HTML

    Args:
        title: TITLE ของหน้า
        headline: ข้อความหลัก
        subheadline: ข้อความรอง
        features: list[ {title, desc} ]
        cta_text, cta_link: ปุ่ม CTA
        hero_bg, hero_text: สีพื้นที่ Hero
        cta_bg, cta_text_color: สีปุ่ม
        features_title: หัวข้อฟีเจอร์
        output_subdir: โฟลเดอร์ย่อยสำหรับเก็บไฟล์

    Returns:
        { "path": "path/to/file.html", "html": "<html...>", "url": "file://..." }
    """
    features = features or [{"title": "ฟีเจอร์ 1", "desc": "รายละเอียด..."}]
    features_html = _render_features(features)

    html = _LANDING_TEMPLATE.format(
        title=title,
        headline=headline,
        subheadline=subheadline,
        features_title=features_title,
        features_html=features_html,
        cta_text=cta_text,
        cta_link=cta_link,
        hero_bg=hero_bg,
        hero_text=hero_text,
        cta_bg=cta_bg,
        cta_text_color=cta_text_color,
        year=datetime.now().year,
    )

    out_dir = _ensure_output_dir(output_subdir)
    slug = title.lower().replace(" ", "-")[:30]
    file_path = out_dir / f"{slug}.html"
    file_path.write_text(html, encoding="utf-8")

    log.info("Landing page created: %s", file_path)
    return {
        "path": str(file_path),
        "html": html,
        "url": f"file://{file_path}",
    }


def generate_html(
    filename: str,
    html_content: str,
    output_subdir: str = "",
) -> dict[str, Any]:
    """
    เขียน HTML ตามที่กำหนด

    Args:
        filename: ชื่อไฟล์ (เช่น 'index.html')
        html_content: เนื้อหา HTML
        output_subdir: โฟลเดอร์ย่อย

    Returns:
        { "path": "...", "url": "file://..." }
    """
    out_dir = _ensure_output_dir(output_subdir)
    file_path = out_dir / filename
    file_path.write_text(html_content, encoding="utf-8")
    log.info("File written: %s", file_path)
    return {"path": str(file_path), "url": f"file://{file_path}"}


def write_file(path: str, content: str) -> dict[str, Any]:
    """
    เขียนไฟล์ไปที่ path ใด ๆ

    Args:
        path: path เต็มหรือ relative จากโปรเจค
        content: เนื้อหาไฟล์

    Returns:
        { "path": "...", "size": 123 }
    """
    full_path = Path(path)
    full_path.parent.mkdir(parents=True, exist_ok=True)
    full_path.write_text(content, encoding="utf-8")
    log.info("File written: %s (%d bytes)", full_path, len(content))
    return {"path": str(full_path), "size": len(content)}


def list_projects() -> list[dict[str, Any]]:
    """แสดงรายการโปรเจคที่สร้างไว้"""
    _OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    projects = []
    for item in _OUTPUT_DIR.iterdir():
        if item.is_dir():
            files = [f.name for f in item.iterdir() if f.suffix == ".html"]
            if files:
                projects.append({
                    "name": item.name,
                    "files": files,
                    "path": str(item),
                })
    # ถ้ายังไม่มีโปรเจค
    if not projects:
        # ตรวจสอบไฟล์ HTML โดยตรง
        for f in _OUTPUT_DIR.glob("*.html"):
            projects.append({
                "name": f.stem,
                "files": [f.name],
                "path": str(_OUTPUT_DIR),
            })
    return projects


# ── Preview Server ────────────────────────────────────────

_preview_server: threading.Thread | None = None
_preview_port: int = 0


def serve_preview(directory: str | None = None, port: int = 3000) -> dict[str, Any]:
    """
    เปิด preview server (HTTP) สำหรับดูเว็บที่สร้าง

    Args:
        directory: path โฟลเดอร์ (default = output/websites/)
        port: พอร์ต

    Returns:
        { "url": "http://localhost:3000", "port": 3000 }
    """
    global _preview_server, _preview_port

    doc_root = Path(directory) if directory else _OUTPUT_DIR
    doc_root.mkdir(parents=True, exist_ok=True)

    if _preview_server and _preview_server.is_alive():
        return {"url": f"http://localhost:{_preview_port}", "port": _preview_port}

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(doc_root), **kwargs)

        def log_message(self, fmt, *args):
            log.info("[preview] %s", fmt % args)

    _preview_port = port
    server = socketserver.TCPServer(("", port), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    _preview_server = thread

    log.info("Preview server at http://localhost:%d", port)
    return {"url": f"http://localhost:{port}", "port": port}
