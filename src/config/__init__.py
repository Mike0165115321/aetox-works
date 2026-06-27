# Aetox Works — Configuration
# อ่านค่าจาก .env ใช้ python-dotenv

import os
from dotenv import load_dotenv

load_dotenv(override=True)  # โหลด .env project ก่อน (overrides system env)


def get_deepseek_api_key() -> str:
    key = os.getenv("DEEPSEEK_API_KEY", "")
    if not key or key == "sk-your-key-here":
        raise ValueError(
            "DEEPSEEK_API_KEY ไม่ได้ตั้งค่า กรุณาใส่ใน .env"
        )
    return key


def get_model_name() -> str:
    return os.getenv("MODEL_NAME", "deepseek-v4-flash")


def get_base_url() -> str:
    return os.getenv("BASE_URL", "https://api.deepseek.com/v1")
