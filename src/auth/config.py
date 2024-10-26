from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthSettings(BaseSettings):
    secret_key: str = Field(default="debug")
    algorithm: str = Field(default="HS256")

    model_config = SettingsConfigDict(env_file=".envtest")


def get_auth_settings():
    return AuthSettings() # type: ignore
