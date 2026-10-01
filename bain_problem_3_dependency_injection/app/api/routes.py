from fastapi import APIRouter

from app.clients.ai_client import AIClient
from app.models.recommendation import RecommendationRequest, RecommendationResponse
from app.repositories.user_repository import UserRepository
from app.services.recommendation import RecommendationService

router = APIRouter()
service = RecommendationService(UserRepository(), AIClient())

@router.post("/recommend", response_model=RecommendationResponse)
async def recommend(request: RecommendationRequest):
    result = await service.recommend(request.user_id)
    return RecommendationResponse(recommendation=result)
