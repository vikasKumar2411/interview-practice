class AIClient:
    async def recommend(self, profile: dict) -> str:
        return f"Recommended content for {profile['segment']} user"
