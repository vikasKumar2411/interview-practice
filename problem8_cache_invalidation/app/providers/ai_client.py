class AIClient:
    async def recommend(self, interests: list[str]) -> str:
        return "Recommended topics: " + ", ".join(interests)
