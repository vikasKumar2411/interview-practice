from app.clients.ai_client import AIClient
from app.repositories.user_repository import UserRepository

class RecommendationService:
    def __init__(self, repository: UserRepository, ai_client: AIClient):
        self.repository = repository
        self.ai_client = ai_client

    async def recommend(self, user_id: int) -> str:
        profile = self.repository.get_profile(user_id)
        return await self.ai_client.recommend(profile)
