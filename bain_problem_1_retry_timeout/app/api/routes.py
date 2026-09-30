from fastapi import APIRouter

from app.models.classification import ClassificationRequest, ClassificationResponse
from app.services.classification import ClassificationService

router = APIRouter()
service = ClassificationService()

@router.post("/classify", response_model=ClassificationResponse)
async def classify(request: ClassificationRequest):
    result = await service.classify(request.text)
    return ClassificationResponse(label=result)
