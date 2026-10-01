from app.repositories.job_repository import JobRepository

class JobService:
    def __init__(self, repository: JobRepository | None = None):
        self.repository = repository or JobRepository()

    def create_job(self, idempotency_key: str, payload: str) -> dict:
        existing_job = self.repository.find_by_idempotency_key(idempotency_key)
        if existing_job is not None:
            return existing_job
        return self.repository.create_job(idempotency_key, payload)
