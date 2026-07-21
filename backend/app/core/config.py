import os
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path


def _load_dotenv() -> None:
    env_path = Path(__file__).resolve().parents[3] / ".env"
    if not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue

        key, value = stripped.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def _split_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


@dataclass(frozen=True)
class Settings:
    app_name: str = "AI LeetCode Coach API"
    app_version: str = "0.1.0"
    app_env: str = "development"
    app_host: str = "127.0.0.1"
    app_port: int = 8000
    log_level: str = "INFO"
    allowed_origins: list[str] = field(default_factory=list)
    allowed_origin_regex: str = r"^(chrome-extension|extension)://[a-z]+$"
    deepseek_api_key: str = ""
    deepseek_base_url: str = "https://api.deepseek.com"
    deepseek_model: str = "deepseek-chat"
    llm_timeout_seconds: float = 30.0
    llm_max_retries: int = 1
    database_url: str = "postgresql+psycopg://leetcode_coach:leetcode_coach@localhost:5432/leetcode_coach"


@lru_cache
def get_settings() -> Settings:
    _load_dotenv()
    origins = _split_csv(os.getenv("ALLOWED_ORIGINS", ""))

    return Settings(
        app_env=os.getenv("APP_ENV", "development"),
        app_host=os.getenv("APP_HOST", "127.0.0.1"),
        app_port=int(os.getenv("APP_PORT", "8000")),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
        allowed_origins=origins,
        deepseek_api_key=os.getenv("DEEPSEEK_API_KEY", ""),
        deepseek_base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
        deepseek_model=os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
        llm_timeout_seconds=float(os.getenv("LLM_TIMEOUT_SECONDS", "30")),
        llm_max_retries=int(os.getenv("LLM_MAX_RETRIES", "1")),
        database_url=os.getenv(
            "DATABASE_URL",
            "postgresql+psycopg://leetcode_coach:leetcode_coach@localhost:5432/leetcode_coach",
        ),
    )
