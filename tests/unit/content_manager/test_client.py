import pytest

from src.content_manager.client import LanguageClient
from src.content_manager.config import get_ai_settings

settings = get_ai_settings()


@pytest.mark.skipif(not settings.api_key, reason="Api key for ai client has not been provided.")
def test_validate_text_as_safe():
    client = LanguageClient(settings.api_key)
    text = "This is not bad but could be better"
    is_safe = client.analyze_text(text)

    assert is_safe


@pytest.mark.skipif(not settings.api_key, reason="Api key for ai client has not been provided.")
def test_validate_text_as_harmfull():
    client = LanguageClient(settings.api_key)
    text = "This is just a garbage. Wasted time..."
    is_safe = client.analyze_text(text)

    assert not is_safe
