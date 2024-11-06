from .client import ILanguageClient, LanguageClient, MockLanguageClient
from .config import get_ai_settings

settings = get_ai_settings()


def get_ai_client() -> ILanguageClient:
    if settings.api_key is None:
        return MockLanguageClient()

    return LanguageClient(api_key=settings.api_key)
