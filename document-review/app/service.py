from app.models import ReviewRequest, ReviewResponse
from app.repository import DocRepository


class ReviewService:
    def __init__(self, repository: DocRepository):
        self.repository = repository

    def create_review(
        self,
        req: ReviewRequest,
    ) -> ReviewResponse:
        return self.repository.save(
            document_name=req.document_name,
            submitted_by=req.submitted_by,
            priority=req.priority,
            status="pending",
        )

    def get_review(
        self,
        review_id: int,
    ) -> ReviewResponse | None:
        return self.repository.get(review_id)