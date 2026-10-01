from app.providers.ai_classifier import AIClassifier


class TicketService:
    def __init__(self, classifier: AIClassifier) -> None:
        self.classifier = classifier

    async def classify_ticket(self, text: str) -> dict:
        return await self.classifier.classify(text)
