from unittest.mock import Mock

from app.repositories.job_repository import JobRepository
from app.services.job_service import JobService

def test_create_job_delegates_to_repository():
    repository = Mock(spec=JobRepository)
    repository.find_by_idempotency_key.return_value = None
    repository.create_job.return_value = {
        "job_id": 1,
        "idempotency_key": "abc-123",
        "payload": "hello",
        "status": "created",
    }

    service = JobService(repository)

    result = service.create_job("abc-123", "hello")

    assert result == repository.create_job.return_value
    repository.find_by_idempotency_key.assert_called_once_with("abc-123")
    repository.create_job.assert_called_once_with("abc-123", "hello")


def test_create_job_returns_existing_job_without_creating_another():
    repository = Mock(spec=JobRepository)
    existing_job = {
        "job_id": 1,
        "idempotency_key": "abc-123",
        "payload": "hello",
        "status": "created",
    }
    repository.find_by_idempotency_key.return_value = existing_job

    service = JobService(repository)

    result = service.create_job("abc-123", "different payload")

    assert result is existing_job
    repository.find_by_idempotency_key.assert_called_once_with("abc-123")
    repository.create_job.assert_not_called()
