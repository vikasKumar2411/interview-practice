from unittest.mock import AsyncMock, Mock

import pytest

from app.clients.ai_client import AIClient
from app.repositories.user_repository import UserRepository
from app.services.recommendation import RecommendationService

@pytest.mark.asyncio
async def test_recommendation_service():
    service = RecommendationService(UserRepository(), AIClient())

    result = await service.recommend(42)

    assert result == "Recommended content for premium user"


@pytest.mark.asyncio
async def test_recommendation_service_with_injected_mocks():
    profile = {"user_id": 42, "segment": "test"}
    repository = Mock(spec=UserRepository)
    repository.get_profile.return_value = profile
    ai_client = AsyncMock(spec=AIClient)
    ai_client.recommend.return_value = "test recommendation"
    service = RecommendationService(repository, ai_client)

    result = await service.recommend(42)

    assert result == "test recommendation"
    repository.get_profile.assert_called_once_with(42)
    ai_client.recommend.assert_awaited_once_with(profile)
