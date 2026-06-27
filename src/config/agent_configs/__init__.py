# Aetox Works — Agent Configs Loader
# โหลด prompt และ config ของ agent แต่ละตัว

import os
import yaml
from typing import Any

_CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))

_cache: dict[str, dict[str, Any]] | None = None


def load_all() -> dict[str, dict[str, Any]]:
    """โหลด config ของ agent ทั้งหมด เรียงตาม order"""
    global _cache
    if _cache is not None:
        return _cache

    configs = {}
    for fname in sorted(os.listdir(_CONFIG_DIR)):
        if not fname.endswith(".yaml"):
            continue
        path = os.path.join(_CONFIG_DIR, fname)
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
            if data and "name" in data:
                configs[data["name"]] = data

    _cache = configs
    return configs


def get_agent_config(name: str) -> dict[str, Any] | None:
    """โหลด config ของ agent ตัวเดียว"""
    return load_all().get(name)


def get_system_prompt(name: str) -> str:
    """ดึง system prompt ของ agent"""
    config = get_agent_config(name)
    if config is None:
        return ""
    return config.get("system_prompt", "")


def get_output_format(name: str) -> str:
    """ดึง output format spec ของ agent"""
    config = get_agent_config(name)
    if config is None:
        return ""
    return config.get("output_format", "")
