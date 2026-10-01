from unittest.mock import AsyncMock, Mock

import pytest

from app.cache import RecommendationCache
from app.providers.ai_client import AIClient
from app.repositories.user_repository import UserRepository
from app.services.recommendation_service import RecommendationService


@pytest.mark.asyncio
async def test_cache_miss_loads_profile_calls_ai_and_caches_result() -> None:
    repository = AsyncMock(spec=UserRepository)
    ai_client = AsyncMock(spec=AIClient)
    cache = Mock(spec=RecommendationCache)

    cache.get.return_value = None
    repository.get_interests.return_value = ["python"]
    ai_client.recommend.return_value = "Learn FastAPI"

    service = RecommendationService(repository, ai_client, cache)

    result = await service.get_recommendation(1)

    assert result == "Learn FastAPI"
    cache.get.assert_called_once_with(1)
    repository.get_interests.assert_awaited_once_with(1)
    ai_client.recommend.assert_awaited_once_with(["python"])
    cache.set.assert_called_once_with(1, "Learn FastAPI")


@pytest.mark.asyncio
async def test_cache_hit_skips_repository_and_ai() -> None:
    repository = AsyncMock(spec=UserRepository)
    ai_client = AsyncMock(spec=AIClient)
    cache = Mock(spec=RecommendationCache)

    cache.get.return_value = "cached recommendation"

    service = RecommendationService(repository, ai_client, cache)

    result = await service.get_recommendation(1)

    assert result == "cached recommendation"
    cache.get.assert_called_once_with(1)
    repository.get_interests.assert_not_awaited()
    ai_client.recommend.assert_not_awaited()
    cache.set.assert_not_called()
