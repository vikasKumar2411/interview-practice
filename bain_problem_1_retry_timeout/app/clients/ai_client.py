import httpx

class AIClient:
    def __init__(self, base_url: str = "https://provider.example.com"):
        self.base_url = base_url

    async def classify(self, text: str) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/classify",
                json={"text": text},
            )
            response.raise_for_status()

        return response.json()["label"]
