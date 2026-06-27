"""Tests for Agent Configs Loader"""

from src.config.agent_configs import load_all, get_agent_config, get_system_prompt


def test_loads_all_five_agents():
    configs = load_all()
    assert set(configs.keys()) == {"sales", "research", "content", "dev", "data"}


def test_each_agent_has_name_and_prompt():
    configs = load_all()
    for name, cfg in configs.items():
        assert cfg["name"] == name
        assert "system_prompt" in cfg
        assert len(cfg["system_prompt"]) > 50


def test_get_agent_config_returns_none_for_unknown():
    assert get_agent_config("nonexistent") is None


def test_sales_prompt_mentions_pain_point():
    prompt = get_system_prompt("sales")
    assert "pain" in prompt.lower()


def test_research_prompt_mentions_competitors():
    prompt = get_system_prompt("research")
    assert "คู่แข่ง" in prompt or "competitor" in prompt.lower()


def test_content_prompt_mentions_copy():
    prompt = get_system_prompt("content")
    assert "copy" in prompt.lower() or "landing" in prompt


def test_dev_prompt_mentions_html():
    prompt = get_system_prompt("dev")
    assert "HTML" in prompt


def test_data_prompt_mentions_analyze():
    prompt = get_system_prompt("data")
    assert "วิเคร" in prompt or "analysis" in prompt.lower()
