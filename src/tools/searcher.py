"""
Aetox Works — Research Tools (Research Agent 🔍)

ค้นหาข้อมูลจากเว็บผ่าน Firecrawl API และ Exa API
"""
import os
import logging
from typing import Any

import httpx

from src.config import get_base_url

log = logging.getLogger("aetox.searcher")

# ── API Keys ──────────────────────────────────────────────


def _firecrawl_key() -> str:
    key = os.getenv("FIRECRAWL_API_KEY", "")
    if not key:
        log.warning("FIRECRAWL_API_KEY not set — search will fail")
    return key


def _exa_key() -> str:
    key = os.getenv("EXA_API_KEY", "")
    if not key:
        log.warning("EXA_API_KEY not set — semantic search will fail")
    return key


# ── Firecrawl Search ──────────────────────────────────────

FIRECRAWL_BASE = "https://api.firecrawl.dev/v1"


def web_search(query: str, num_results: int = 5) -> list[dict[str, Any]]:
    """
    ค้นหาข้อมูลจากเว็บด้วย Firecrawl Search API (synchronous)

    Args:
        query: คำค้นหา
        num_results: จำนวนผลลัพธ์ (1-20)

    Returns:
        list[ {title, url, description, content} ]
    """
    key = _firecrawl_key()
    if not key:
        return _demo_results(query, "firecrawl")

    try:
        with httpx.Client(timeout=30) as client:
            resp = client.post(
                f"{FIRECRAWL_BASE}/search",
                headers={
                    "Authorization": f"Bearer {key}",
                    "Content-Type": "application/json",
                },
                json={
                    "query": query,
                    "limit": min(num_results, 20),
                    "scrapeOptions": {"formats": ["markdown"]},
                },
            )
            resp.raise_for_status()
            data = resp.json()
            results = []
            for item in (data.get("data", {}).get("results", []) or []):
                results.append({
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "description": item.get("description", ""),
                    "content": item.get("markdown", "")[:2000],
                })
            log.info("Firecrawl search '%s' → %d results", query, len(results))
            return results
    except Exception as e:
        log.warning("Firecrawl search error: %s", e)
        return _demo_results(query, "firecrawl")


def scrape_url(url: str) -> str:
    """
    ดึงเนื้อหาจาก URL ด้วย Firecrawl (synchronous)

    Args:
        url: ลิงก์ที่ต้องการดึงข้อมูล

    Returns:
        markdown content
    """
    key = _firecrawl_key()
    if not key:
        return f"[Firecrawl DEMO] Scraped: {url}"

    try:
        with httpx.Client(timeout=30) as client:
            resp = client.post(
                f"{FIRECRAWL_BASE}/scrape",
                headers={
                    "Authorization": f"Bearer {key}",
                    "Content-Type": "application/json",
                },
                json={
                    "url": url,
                    "formats": ["markdown"],
                    "onlyMainContent": True,
                },
            )
            resp.raise_for_status()
            data = resp.json()
            content = (data.get("data", {}) or {}).get("markdown", "")
            log.info("Scraped %s → %d chars", url, len(content))
            return content[:5000]  # จำกัดไม่ให้ใหญ่เกิน
    except Exception as e:
        log.warning("Scrape error %s: %s", url, e)
        return f"[Scrape Error] {url}: {e}"


# ── Exa Semantic Search ───────────────────────────────────

EXA_BASE = "https://api.exa.ai"


def semantic_search(query: str, num_results: int = 5) -> list[dict[str, Any]]:
    """
    Semantic search ด้วย Exa API (synchronous)
    เหมาะกับค้นหา insight / content ที่เกี่ยวข้อง

    Args:
        query: คำค้นหาแบบ semantic
        num_results: จำนวนผลลัพธ์

    Returns:
        list[ {title, url, text} ]
    """
    key = _exa_key()
    if not key:
        return _demo_results(query, "exa")

    try:
        with httpx.Client(timeout=30) as client:
            resp = client.post(
                f"{EXA_BASE}/search",
                headers={
                    "Authorization": f"Bearer {key}",
                    "Content-Type": "application/json",
                },
                json={
                    "query": query,
                    "numResults": min(num_results, 20),
                    "contents": {"text": {"maxCharacters": 2000}},
                },
            )
            resp.raise_for_status()
            data = resp.json()
            results = []
            for item in data.get("results", []):
                results.append({
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "text": (item.get("text", "") or "")[:2000],
                })
            log.info("Exa search '%s' → %d results", query, len(results))
            return results
    except Exception as e:
        log.warning("Exa search error: %s", e)
        return _demo_results(query, "exa")


# ── Fallback DEMO (เมื่อไม่มี API key) ─────────────────────

_demo_counter = 0


def _demo_results(query: str, source: str) -> list[dict[str, Any]]:
    """คืนข้อความ DEMO เมื่อไม่มี API key"""
    global _demo_counter
    _demo_counter += 1
    log.info("[DEMO] %s search for '%s' (no API key)", source, query)
    return [{
        "title": f"[{source.upper()} DEMO] Result for: {query}",
        "url": "https://example.com",
        "description": f"นี่คือผลการค้นหา DEMO จาก {source.upper()} "
                       f"(กรุณาใส่ API key ใน .env)\n"
                       f"คำค้นหา: {query}",
        "content": f"นี่คือเนื้อหา DEMO ที่แสดงเมื่อไม่มี API key\n"
                   f"ถ้าต้องการใช้งานจริง กรุณาใส่ FIRECRAWL_API_KEY "
                   f"หรือ EXA_API_KEY ในไฟล์ .env",
    }]
