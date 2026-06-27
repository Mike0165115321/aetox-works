# Aetox Works — LLM Client
# เรียก DeepSeek API (OpenAI-compatible)

import httpx
from src.config import get_deepseek_api_key, get_model_name, get_base_url

_TIMEOUT = 30.0


def call_llm(
    prompt: str,
    system_prompt: str | None = None,
    model: str | None = None,
) -> str:
    """ส่ง prompt ไปให้ LLM แล้วคืนคำตอบ"""
    api_key = get_deepseek_api_key()
    model = model or get_model_name()
    base_url = get_base_url()

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    try:
        with httpx.Client(timeout=_TIMEOUT) as client:
            resp = client.post(
                f"{base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model,
                    "messages": messages,
                    "temperature": 0.3,  # ให้ deterministic
                },
            )
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"].strip()

    except httpx.TimeoutException:
        return "[LLM Timeout — ลองใหม่อีกครั้ง]"
    except httpx.HTTPStatusError as e:
        return f"[LLM Error {e.response.status_code}]"
    except Exception as e:
        return f"[LLM Error: {e}]"
