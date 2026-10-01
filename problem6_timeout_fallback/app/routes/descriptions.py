from fastapi import APIRouter

from app.models import DescriptionRequest, DescriptionResponse
from app.providers.primary_ai import PrimaryAIProvider
from app.providers.fallback_ai import FallbackAIProvider
from app.services.description_service import DescriptionService


router = APIRouter()

primary_provider = PrimaryAIProvider()
fallback_provider = FallbackAIProvider()

service = DescriptionService(
    primary_provider=primary_provider,
    fallback_provider=fallback_provider,
)


@router.post(
    "/descriptions",
    response_model=DescriptionResponse,
)
async def create_description(
    request: DescriptionRequest,
) -> DescriptionResponse:
    description = await service.generate_description(
        request.product_name,
        request.features,
    )
    return DescriptionResponse(description=description)
