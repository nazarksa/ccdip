from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Typed runtime configuration loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    app_name: str = "Saudi Construction Dependency Intelligence Platform"
    environment: Literal["local", "development", "test", "staging", "production"] = "local"
    debug: bool = False
    api_prefix: str = "/api/v1"
    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:5173"])

    database_url: str = "postgresql+asyncpg://ccdip:ccdip@localhost:5432/ccdip"
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_username: str = "neo4j"
    neo4j_password: str = "local-development-only"
    redis_url: str = "redis://localhost:6379/0"

    azure_openai_endpoint: str | None = None
    azure_openai_api_key: str | None = None
    azure_openai_api_version: str | None = None
    azure_openai_chat_deployment: str | None = None
    azure_openai_embedding_deployment: str | None = None

    storage_endpoint: str = "http://localhost:9000"
    storage_bucket: str = "ccdip-documents"
    storage_access_key: str = "minio"
    storage_secret_key: str = "local-development-only"


@lru_cache
def get_settings() -> Settings:
    return Settings()
