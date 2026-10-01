from pydantic import ValidationError

from app.exceptions import InvalidAIResponseError
from app.models import TicketClassification
from app.providers.ai_classifier import AIClassifier


class TicketService:
    def __init__(self, classifier: AIClassifier) -> None:
        self.classifier = classifier

    async def classify_ticket(self, text: str) -> dict:
        payload = await self.classifier.classify(text)
        try:
            classification = TicketClassification.model_validate(payload)
        except ValidationError as exc:
            raise InvalidAIResponseError(payload) from exc
        return classification.model_dump()
