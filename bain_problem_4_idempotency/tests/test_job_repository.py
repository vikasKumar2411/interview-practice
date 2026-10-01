from app.repositories.job_repository import JobRepository

def test_create_job():
    repository = JobRepository()

    job = repository.create_job("abc-123", "hello")

    assert job["job_id"] == 1
    assert job["idempotency_key"] == "abc-123"
    assert job["payload"] == "hello"
    assert job["status"] == "created"

def test_find_by_idempotency_key():
    repository = JobRepository()
    repository.create_job("abc-123", "hello")

    job = repository.find_by_idempotency_key("abc-123")

    assert job is not None
    assert job["idempotency_key"] == "abc-123"
