from app.models import ReviewRequest
from app.repository import DocRepository
from app.service import ReviewService


def build_service() -> ReviewService:
    repository = DocRepository()
    return ReviewService(repository)


def test_create_review_sets_pending_status():
    service = build_service()

    review = service.create_review(
        ReviewRequest(
            document_name="contract.pdf",
            submitted_by="user@example.com",
        )
    )

    assert review.status == "pending"
    assert review.id == 1


def test_second_review_gets_new_id():
    service = build_service()

    first = service.create_review(
        ReviewRequest(
            document_name="contract.pdf",
            submitted_by="user@example.com",
        )
    )

    second = service.create_review(
        ReviewRequest(
            document_name="nda.pdf",
            submitted_by="user2@example.com",
            priority="high",
        )
    )

    assert first.id == 1
    assert second.id == 2


def test_get_existing_review():
    service = build_service()

    created = service.create_review(
        ReviewRequest(
            document_name="contract.pdf",
            submitted_by="user@example.com",
        )
    )

    retrieved = service.get_review(created.id)

    assert retrieved == created


def test_get_missing_review_returns_none():
    service = build_service()

    review = service.get_review(999)

    assert review is None