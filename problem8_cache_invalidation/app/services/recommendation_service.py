from app.cache import RecommendationCache
from app.providers.ai_client import AIClient
from app.repositories.user_repository import UserRepository


class RecommendationService:
    def __init__(
        self,
        repository: UserRepository,
        ai_client: AIClient,
        cache: RecommendationCache,
    ) -> None:
        self.repository = repository
        self.ai_client = ai_client
        self.cache = cache

    async def get_recommendation(self, user_id: int) -> str:
        cached = self.cache.get(user_id)
        if cached is not None:
            return cached

        interests = await self.repository.get_interests(user_id)
        recommendation = await self.ai_client.recommend(interests)
        self.cache.set(user_id, recommendation)
        return recommendation
