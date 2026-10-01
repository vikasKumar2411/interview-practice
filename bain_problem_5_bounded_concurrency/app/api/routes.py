from fastapi import APIRouter

from app.models.batch import BatchRequest, BatchResponse
from app.services.batch_service import BatchService


router = APIRouter()
service = BatchService()


@router.post("/batch", response_model=BatchResponse)
async def process_batch(request: BatchRequest):
    results = await service.process_items(request.items)
    return BatchResponse(results=results)
