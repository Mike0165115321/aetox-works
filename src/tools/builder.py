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

# Modern template with animations, gradient hero, card hover effects
_TEMPLATE_MODERN = r"""<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
  :root {{
    --ink: #1a1a2e;
    --surface: #ffffff;
    --muted: #f5f5f7;
    --accent: #e94560;
    --accent-glow: rgba(233,69,96,0.4);
    --hero-bg: linear-gradient(135deg, #0f0f23 0%, #1a1a3e 50%, #16213e 100%);
    --card-bg: #ffffff;
    --card-shadow: 0 1px 3px rgba(0,0,0,0.08);
    --card-hover-shadow: 0 12px 40px rgba(0,0,0,0.12);
    --radius: 12px;
    --max-width: 1100px;
  }}

  * {{ box-sizing: border-box; margin: 0; padding: 0; }}

  html {{ scroll-behavior: smooth; }}

  body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Noto Sans Thai', 'Segoe UI', sans-serif;
    line-height: 1.7;
    color: var(--ink);
    background: var(--surface);
    -webkit-font-smoothing: antialiased;
  }}

  /* ── Nav ── */
  .nav {{
    position: fixed; top: 0; left: 0; right: 0; z-index: 100;
    background: rgba(255,255,255,0.85); backdrop-filter: blur(12px);
    border-bottom: 1px solid rgba(0,0,0,0.06);
    padding: 0 24px;
  }}
  .nav-inner {{
    max-width: var(--max-width); margin: 0 auto;
    display: flex; align-items: center; justify-content: space-between;
    height: 60px;
  }}
  .nav-logo {{ font-weight: 700; font-size: 1.2em; color: var(--ink); text-decoration: none; }}
  .nav-cta {{
    padding: 8px 20px; background: var(--accent); color: #fff;
    border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 0.9em;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }}
  .nav-cta:hover {{ transform: translateY(-1px); box-shadow: 0 4px 16px var(--accent-glow); }}

  /* ── Hero ── */
  .hero {{
    background: var(--hero-bg);
    color: #ffffff;
    padding: 140px 24px 100px;
    text-align: center;
    position: relative;
    overflow: hidden;
  }}
  .hero::before {{
    content: '';
    position: absolute; inset: 0;
    background: radial-gradient(circle at 30% 50%, rgba(233,69,96,0.15) 0%, transparent 60%),
                radial-gradient(circle at 70% 30%, rgba(99,102,241,0.1) 0%, transparent 50%);
  }}
  .hero-content {{ position: relative; z-index: 1; max-width: 720px; margin: 0 auto; }}
  .hero h1 {{
    font-size: clamp(2rem, 5vw, 3.8rem);
    font-weight: 800;
    line-height: 1.15;
    letter-spacing: -0.02em;
    margin-bottom: 20px;
    animation: fadeInUp 0.8s ease-out;
  }}
  .hero p {{
    font-size: clamp(1rem, 2vw, 1.25rem);
    opacity: 0.85;
    max-width: 560px;
    margin: 0 auto 36px;
    line-height: 1.7;
    animation: fadeInUp 0.8s ease-out 0.15s both;
  }}
  .hero .cta-btn {{
    display: inline-block; padding: 16px 40px;
    background: var(--accent); color: #fff;
    text-decoration: none; border-radius: 10px;
    font-size: 1.1em; font-weight: 700;
    transition: transform 0.25s cubic-bezier(0.34,1.56,0.64,1),
                box-shadow 0.25s ease;
    animation: fadeInUp 0.8s ease-out 0.3s both;
  }}
  .hero .cta-btn:hover {{
    transform: translateY(-2px) scale(1.03);
    box-shadow: 0 8px 30px var(--accent-glow);
  }}

  /* ── Sections ── */
  .section {{
    max-width: var(--max-width); margin: 0 auto; padding: 80px 24px;
  }}
  .section-label {{
    text-transform: uppercase; letter-spacing: 0.08em; font-size: 0.8em;
    font-weight: 700; color: var(--accent); margin-bottom: 8px;
  }}
  .section h2 {{
    font-size: clamp(1.6rem, 3.5vw, 2.4rem);
    font-weight: 800; letter-spacing: -0.02em;
    margin-bottom: 16px; line-height: 1.25;
  }}
  .section-desc {{
    color: #555; font-size: 1.05em; max-width: 600px;
    margin-bottom: 48px; line-height: 1.65;
  }}

  /* ── Features Grid ── */
  .features-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 24px;
  }}
  .feature-card {{
    background: var(--card-bg);
    border-radius: var(--radius);
    padding: 32px 28px;
    box-shadow: var(--card-shadow);
    border: 1px solid rgba(0,0,0,0.04);
    transition: transform 0.3s cubic-bezier(0.34,1.56,0.64,1),
                box-shadow 0.3s ease;
    animation: fadeInUp 0.6s ease-out both;
  }}
  .feature-card:hover {{
    transform: translateY(-6px);
    box-shadow: var(--card-hover-shadow);
  }}
  .feature-icon {{
    width: 48px; height: 48px; border-radius: 12px;
    background: linear-gradient(135deg, var(--accent), #ff6b81);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.4em; margin-bottom: 20px; color: #fff;
  }}
  .feature-card h3 {{
    font-size: 1.15em; font-weight: 700; margin-bottom: 8px;
  }}
  .feature-card p {{
    color: #555; font-size: 0.95em; line-height: 1.6;
  }}

  /* ── CTA Section ── */
  .cta-section {{
    background: var(--muted);
    text-align: center;
    padding: 80px 24px;
  }}
  .cta-section h2 {{
    font-size: clamp(1.5rem, 3.5vw, 2.2rem);
    font-weight: 800; margin-bottom: 12px;
  }}
  .cta-section p {{
    color: #555; font-size: 1.05em; max-width: 500px;
    margin: 0 auto 28px;
  }}
  .cta-section .cta-btn {{
    display: inline-block; padding: 16px 40px;
    background: var(--accent); color: #fff;
    text-decoration: none; border-radius: 10px;
    font-size: 1.1em; font-weight: 700;
    transition: transform 0.25s cubic-bezier(0.34,1.56,0.64,1),
                box-shadow 0.25s ease;
  }}
  .cta-section .cta-btn:hover {{
    transform: translateY(-2px) scale(1.03);
    box-shadow: 0 8px 30px var(--accent-glow);
  }}

  /* ── Footer ── */
  .footer {{
    text-align: center; padding: 48px 24px;
    color: #888; font-size: 0.9em;
    border-top: 1px solid rgba(0,0,0,0.06);
  }}

  /* ── Keyframes ── */
  @keyframes fadeInUp {{
    from {{ opacity: 0; transform: translateY(24px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
  }}

  /* ── Accessibility ── */
  @media (prefers-reduced-motion: reduce) {{
    *, *::before, *::after {{
      animation-duration: 0.01ms !important;
      transition-duration: 0.01ms !important;
    }}
    html {{ scroll-behavior: auto; }}
  }}

  /* ── Responsive ── */
  @media (max-width: 768px) {{
    .hero {{ padding: 120px 20px 80px; }}
    .hero h1 {{ font-size: clamp(1.8rem, 7vw, 2.5rem); }}
    .section {{ padding: 60px 20px; }}
    .features-grid {{ grid-template-columns: 1fr; }}
  }}
</style>
</head>
<body>
  <nav class="nav">
    <div class="nav-inner">
      <a href="#" class="nav-logo">{title}</a>
      <a href="#cta" class="nav-cta">{cta_text}</a>
    </div>
  </nav>

  <section class="hero">
    <div class="hero-content">
      <h1>{headline}</h1>
      <p>{subheadline}</p>
      <a href="#cta" class="cta-btn">{cta_text}</a>
    </div>
  </section>

  <section class="section">
    <p class="section-label">{features_title}</p>
    <h2>สิ่งที่คุณจะได้รับ</h2>
    <p class="section-desc">{subheadline}</p>
    <div class="features-grid">
      {features_html}
    </div>
  </section>

  <section class="cta-section" id="cta">
    <h2>พร้อมเริ่มต้นหรือยัง?</h2>
    <p>{subheadline}</p>
    <a href="{cta_link}" class="cta-btn">{cta_text}</a>
  </section>

  <footer class="footer">
    <p>© {year} {title} — สร้างโดย Aetox Works Dev Agent</p>
  </footer>
</body>
</html>"""


# Minimal template — clean, professional, no frills
_TEMPLATE_MINIMAL = r"""<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
  :root {{
    --ink: #1a1a2e; --surface: #fafafa; --card: #ffffff;
    --accent: #2563eb; --muted: #e5e7eb; --radius: 8px;
    --max-width: 960px;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: -apple-system, 'Noto Sans Thai', 'Segoe UI', sans-serif;
    line-height: 1.7; color: var(--ink); background: var(--surface);
  }}
  .hero {{
    text-align: center; padding: 100px 24px 64px;
    max-width: var(--max-width); margin: 0 auto;
  }}
  .hero h1 {{
    font-size: clamp(1.8rem, 4vw, 2.8rem);
    font-weight: 800; letter-spacing: -0.02em; margin-bottom: 16px;
  }}
  .hero p {{ color: #555; font-size: 1.1em; max-width: 540px; margin: 0 auto 32px; }}
  .cta-btn {{
    display: inline-block; padding: 14px 36px;
    background: var(--accent); color: #fff;
    text-decoration: none; border-radius: var(--radius);
    font-weight: 600; font-size: 1em;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }}
  .cta-btn:hover {{ transform: translateY(-2px); box-shadow: 0 6px 20px rgba(37,99,235,0.3); }}
  .section {{ max-width: var(--max-width); margin: 0 auto; padding: 48px 24px; }}
  .section h2 {{
    font-size: 1.6em; font-weight: 700; margin-bottom: 32px;
  }}
  .features-grid {{
    display: grid; gap: 20px;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  }}
  .feature-card {{
    background: var(--card); border-radius: var(--radius);
    padding: 28px 24px;
    border: 1px solid var(--muted);
    transition: border-color 0.25s ease;
  }}
  .feature-card:hover {{ border-color: var(--accent); }}
  .feature-card h3 {{ font-size: 1.05em; margin-bottom: 8px; }}
  .feature-card p {{ color: #555; font-size: 0.95em; }}
  .footer {{
    text-align: center; padding: 40px 24px;
    color: #888; font-size: 0.9em;
    border-top: 1px solid var(--muted);
  }}
</style>
</head>
<body>
  <section class="hero">
    <h1>{headline}</h1>
    <p>{subheadline}</p>
    <a href="{cta_link}" class="cta-btn">{cta_text}</a>
  </section>
  <section class="section">
    <h2>{features_title}</h2>
    <div class="features-grid">{features_html}</div>
  </section>
  <footer class="footer">
    <p>© {year} {title}</p>
  </footer>
</body>
</html>"""


_TEMPLATES = {
    "modern": _TEMPLATE_MODERN,
    "minimal": _TEMPLATE_MINIMAL,
}

# Icon emoji per feature index
_FEATURE_ICONS = ["🚀", "⚡", "🎯", "🔒", "📊", "💡", "🌟", "🛡️"]


def _render_features(features: list[dict[str, str]], template: str = "modern") -> str:
    """render feature cards HTML with stagger animation delay"""
    cards = []
    for i, f in enumerate(features):
        icon = _FEATURE_ICONS[i % len(_FEATURE_ICONS)]
        if template == "modern":
            cards.append(
                f'<div class="feature-card" style="animation-delay: {i * 0.1}s">'
                f'<div class="feature-icon">{icon}</div>'
                f'<h3>{f.get("title", "")}</h3>'
                f'<p>{f.get("desc", "")}</p></div>'
            )
        else:
            cards.append(
                f'<div class="feature-card">'
                f'<h3>{f.get("title", "")}</h3>'
                f'<p>{f.get("desc", "")}</p></div>'
            )
    return "\n".join(cards)


def _safe_or(val: str, default: str) -> str:
    """Helper: return val if truthy, else default (for template placeholders)"""
    return val if val else default


def generate_landing(
    title: str = "Landing Page",
    headline: str = "\u0e2b\u0e31\u0e27\u0e02\u0e49\u0e2d\u0e2b\u0e25\u0e31\u0e01",
    subheadline: str = "\u0e04\u0e33\u0e2d\u0e18\u0e34\u0e1a\u0e32\u0e22\u0e2a\u0e31\u0e49\u0e19 \u0e46",
    features: list[dict[str, str]] | None = None,
    cta_text: str = "\u0e40\u0e23\u0e34\u0e48\u0e21\u0e15\u0e49\u0e19\u0e40\u0e25\u0e22",
    cta_link: str = "#",
    features_title: str = "\u0e1f\u0e35\u0e40\u0e08\u0e2d\u0e23\u0e4c\u0e02\u0e2d\u0e07\u0e40\u0e23\u0e32",
    output_subdir: str = "",
    template: str = "modern",
) -> dict[str, Any]:
    """
    \u0e2a\u0e23\u0e49\u0e32\u0e07 Landing Page HTML \u0e14\u0e49\u0e27\u0e22 template \u0e17\u0e35\u0e48\u0e40\u0e25\u0e37\u0e2d\u0e01\u0e44\u0e14\u0e49

    Args:
        title: TITLE \u0e02\u0e2d\u0e07\u0e2b\u0e19\u0e49\u0e32
        headline: \u0e02\u0e49\u0e2d\u0e04\u0e27\u0e32\u0e21\u0e2b\u0e25\u0e31\u0e01
        subheadline: \u0e02\u0e49\u0e2d\u0e04\u0e27\u0e32\u0e21\u0e23\u0e2d\u0e07
        features: list[ {title, desc} ]
        cta_text, cta_link: \u0e1b\u0e38\u0e48\u0e21 CTA
        features_title: \u0e2b\u0e31\u0e27\u0e02\u0e49\u0e2d\u0e1f\u0e35\u0e40\u0e08\u0e2d\u0e23\u0e4c
        output_subdir: \u0e42\u0e1f\u0e25\u0e40\u0e14\u0e2d\u0e23\u0e4c\u0e22\u0e48\u0e2d\u0e22\u0e2a\u0e33\u0e2b\u0e23\u0e31\u0e1a\u0e40\u0e01\u0e47\u0e1a\u0e44\u0e1f\u0e25\u0e4c
        template: "modern" (animations, gradient) \u0e2b\u0e23\u0e37\u0e2d "minimal" (clean, professional)

    Returns:
        { "path": "...", "html": "...", "url": "file://..." }
    """
    features = features or [{"title": "\u0e1f\u0e35\u0e40\u0e08\u0e2d\u0e23\u0e4c 1", "desc": "\u0e23\u0e32\u0e22\u0e25\u0e30\u0e40\u0e2d\u0e35\u0e22\u0e14..."}]
    features_html = _render_features(features, template)

    tpl = _TEMPLATES.get(template, _TEMPLATE_MODERN)

    html = tpl.format(
        title=title,
        headline=headline,
        subheadline=subheadline,
        features_title=features_title,
        features_html=features_html,
        cta_text=cta_text,
        cta_link=cta_link,
        year=datetime.now().year,
    )

    out_dir = _ensure_output_dir(output_subdir)
    slug = title.lower().replace(" ", "-")[:40]
    file_path = out_dir / f"{slug}.html"
    file_path.write_text(html, encoding="utf-8")

    log.info("Landing page created [%s]: %s", template, file_path)
    return {
        "path": str(file_path),
        "html": html,
        "url": f"file://{file_path}",
        "template": template,
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


def write_project_file(filename: str, content: str, output_subdir: str = "") -> dict[str, Any]:
    """Write a generated project file under the configured output directory."""
    out_dir = _ensure_output_dir(output_subdir)
    safe_name = Path(filename).name
    return write_file(str(out_dir / safe_name), content)


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


def get_project(name: str) -> dict[str, Any] | None:
    """Read one generated project and include HTML file contents for admin preview."""
    _OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    safe_name = Path(name).name
    target_dir = _OUTPUT_DIR / safe_name

    if target_dir.is_dir():
        files = [f for f in target_dir.iterdir() if f.is_file()]
        return {
            "name": target_dir.name,
            "path": str(target_dir),
            "files": [_project_file_payload(f) for f in files],
        }

    direct_file = _OUTPUT_DIR / f"{safe_name}.html"
    if direct_file.is_file():
        return {
            "name": direct_file.stem,
            "path": str(_OUTPUT_DIR),
            "files": [_project_file_payload(direct_file)],
        }

    return None


def delete_project_file(project_name: str, file_name: str) -> bool:
    """Delete one generated project file, constrained to the output directory."""
    _OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    safe_project = Path(project_name).name
    safe_file = Path(file_name).name
    if not safe_project or not safe_file:
        return False
    if safe_project != project_name or safe_file != file_name:
        return False

    target_dir = _OUTPUT_DIR / safe_project
    if target_dir.is_dir():
        target = target_dir / safe_file
    else:
        direct_file = _OUTPUT_DIR / f"{safe_project}.html"
        target = direct_file if direct_file.name == safe_file else _OUTPUT_DIR / safe_file

    try:
        resolved_output = _OUTPUT_DIR.resolve()
        resolved_target = target.resolve()
    except FileNotFoundError:
        return False

    if resolved_output not in resolved_target.parents and resolved_target != resolved_output:
        return False
    if not resolved_target.is_file():
        return False
    resolved_target.unlink()
    return True


def _project_file_payload(path: Path) -> dict[str, Any]:
    content = ""
    if path.suffix.lower() in {".html", ".htm", ".css", ".js", ".txt", ".md", ".py"}:
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = ""
    return {
        "name": path.name,
        "path": str(path),
        "size": path.stat().st_size,
        "content": content,
        "is_html": path.suffix.lower() in {".html", ".htm"},
    }


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
