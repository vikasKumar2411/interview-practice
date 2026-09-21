from fastapi import APIRouter, HTTPException, status
from app.service import ReviewService
from app.models import ReviewRequest, ReviewResponse
from app.repository import DocRepository

router = APIRouter()
repository = DocRepository()
review_service = ReviewService(repository)

@router.post(
    "/reviews",
    response_model=ReviewResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_review(request: ReviewRequest) -> ReviewResponse:
    return review_service.create_review(request)

@router.get(
    "/reviews/{review_id}",
    response_model=ReviewResponse,
)
def get_review(review_id: int) -> ReviewResponse:
    review = review_service.get_review(review_id)

    if review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found",
        )

    return review