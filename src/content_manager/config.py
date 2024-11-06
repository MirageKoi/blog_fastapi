from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class AIClientSettings(BaseSettings):
    api_key: str | None = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

@lru_cache
def get_ai_settings():
    return AIClientSettings()  # type: ignore
