from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthSettings(BaseSettings):
    secret_key: str = Field(default="development")
    algorithm: str = Field(default="HS256")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


def get_auth_settings():
    return AuthSettings() # type: ignore
