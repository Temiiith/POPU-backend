from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "POPU API"
    app_version: str = "0.1.0"
    environment: str = "development"
    data_mode: str = "synthetic_demo"

    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    database_url: str

    gemini_api_key: str | None = None
    openai_api_key: str | None = None
    anthropic_api_key: str | None = None

    natlas_endpoint_url: str | None = None
    natlas_api_key: str | None = None
    natlas_model: str = "NCAIR1/N-ATLaS"

    llm_primary_provider: str = "gemini"
    llm_model_gemini: str = "gemini-3.8-flash"
    llm_model_openai: str = "gpt-5-mini"
    llm_model_anthropic: str = "claude-sonnet-4-5"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()