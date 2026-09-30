import asyncio

import httpx

from app.clients.ai_client import AIClient
from app.errors import ClassificationUnavailableError

class ClassificationService:
    def __init__(self, client: AIClient | None = None):
        self.client = client or AIClient()
    
    async def classify(self, text: str) -> str:
        for attempt in range(2):
            try:
                return await asyncio.wait_for(self.client.classify(text), timeout=2.0)
            except (TimeoutError, httpx.TimeoutException) as exc:
                if attempt == 1:
                    raise ClassificationUnavailableError("classification unavailable") from exc
