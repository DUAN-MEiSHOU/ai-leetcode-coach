import os
from dataclasses import dataclass, field
from functools import lru_cache


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


@lru_cache
def get_settings() -> Settings:
    origins = _split_csv(os.getenv("ALLOWED_ORIGINS", ""))

    return Settings(
        app_env=os.getenv("APP_ENV", "development"),
        app_host=os.getenv("APP_HOST", "127.0.0.1"),
        app_port=int(os.getenv("APP_PORT", "8000")),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
        allowed_origins=origins,
    )
