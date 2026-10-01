from fastapi import APIRouter

from app.cache import RecommendationCache
from app.models import RecommendationResponse, UserResponse, UserUpdateRequest
from app.providers.ai_client import AIClient
from app.repositories.user_repository import UserRepository
from app.services.recommendation_service import RecommendationService
from app.services.user_service import UserService


router = APIRouter()

repository = UserRepository()
ai_client = AIClient()
cache = RecommendationCache()

recommendation_service = RecommendationService(
    repository=repository,
    ai_client=ai_client,
    cache=cache,
)
user_service = UserService(repository=repository)


@router.get(
    "/users/{user_id}/recommendation",
    response_model=RecommendationResponse,
)
async def get_recommendation(user_id: int) -> RecommendationResponse:
    recommendation = await recommendation_service.get_recommendation(user_id)
    return RecommendationResponse(recommendation=recommendation)


@router.put(
    "/users/{user_id}",
    response_model=UserResponse,
)
async def update_user(
    user_id: int,
    request: UserUpdateRequest,
) -> UserResponse:
    interests = await user_service.update_interests(
        user_id,
        request.interests,
    )
    return UserResponse(
        user_id=user_id,
        interests=interests,
    )
