from google.cloud import language_v1


class LanguageClient:
    def __init__(self, api_key: str) -> None:
        self.client = language_v1.LanguageServiceClient(client_options={"api_key": api_key})

    def _is_content_safe(self, data: language_v1.ModerateTextResponse, threshold: float = 0.5) -> bool:
        for category in data.moderation_categories:
            if category.confidence > threshold:
                return False

        return True

    def analyze_text(self, text: str) -> bool:
        document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
        response = self.client.moderate_text(document=document)
        is_safe = self._is_content_safe(response)

        return is_safe
