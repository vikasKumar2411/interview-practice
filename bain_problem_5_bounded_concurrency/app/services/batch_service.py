import asyncio

from app.clients.ai_client import AIClient


class BatchService:
    def __init__(self, client: AIClient | None = None):
        self.client = client or AIClient()
        self._semaphore = asyncio.Semaphore(3)

    async def process_items(self, items: list[str]) -> list[dict]:
        async def process_item(item: str) -> dict:
            async with self._semaphore:
                try:
                    result = await self.client.process(item)
                except Exception as exc:
                    return {"item": item, "result": None, "error": str(exc)}

            return {"item": item, "result": result, "error": None}

        return await asyncio.gather(*(process_item(item) for item in items))
