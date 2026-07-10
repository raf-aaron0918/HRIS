import json
import json
from functools import lru_cache
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[3]
BACKEND_DIR = PROJECT_ROOT / "backend"
ENV_FILE = BACKEND_DIR / ".env"
LOCAL_DATABASE_URL = f"sqlite:///{(BACKEND_DIR / 'hris.db').as_posix()}"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE, env_file_encoding="utf-8", case_sensitive=False)

    app_name: str = Field(default="HRIS API", alias="APP_NAME")
    app_env: str = Field(default="development", alias="APP_ENV")
    app_debug: bool = Field(default=True, alias="APP_DEBUG")
    api_v1_prefix: str = Field(default="/api/v1", alias="API_V1_PREFIX")
    secret_key: str = Field(default="change-this-secret-key", alias="SECRET_KEY")
    access_token_expire_minutes: int = Field(default=120, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    backend_cors_origins: list[str] = Field(
        default=[
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://localhost:4173",
            "http://127.0.0.1:4173",
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ],
        alias="BACKEND_CORS_ORIGINS",
    )
    database_url: str = Field(default=LOCAL_DATABASE_URL, alias="DATABASE_URL")
    fallback_database_url: str = Field(default=LOCAL_DATABASE_URL, alias="FALLBACK_DATABASE_URL")

    @field_validator("backend_cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            stripped_value = value.strip()
            if stripped_value.startswith("["):
                parsed_value = json.loads(stripped_value)
                return [str(item).strip() for item in parsed_value if str(item).strip()]
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    @field_validator("database_url", "fallback_database_url", mode="before")
    @classmethod
    def normalize_database_url(cls, value: str) -> str:
        if isinstance(value, str) and value.startswith("postgresql://") and not value.startswith("postgresql+"):
            return value.replace("postgresql://", "postgresql+psycopg://", 1)
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
