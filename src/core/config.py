"""Application settings loaded from the environment."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration.

    Values come from environment variables or a local ``.env`` file.
    The Gemini model name is never hardcoded; set ``GEMINI_MODEL``.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    llm_provider: str = "gemini"
    google_api_key: str = ""
    gemini_model: str = ""
    log_level: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    """Return cached settings."""
    return Settings()
