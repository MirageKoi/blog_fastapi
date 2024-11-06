from pydantic_settings import BaseSettings, SettingsConfigDict



class OpenAIAPIKey(BaseSettings):
    api_key: str

    model_config = SettingsConfigDict(env_file=".env")



def get_openai_settings():
    return OpenAIAPIKey()  # type: ignore