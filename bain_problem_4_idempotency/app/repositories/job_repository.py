class JobRepository:
    def __init__(self):
        self.jobs = []
        self._next_id = 1

    def create_job(self, idempotency_key: str, payload: str) -> dict:
        job = {
            "job_id": self._next_id,
            "idempotency_key": idempotency_key,
            "payload": payload,
            "status": "created",
        }
        self._next_id += 1
        self.jobs.append(job)
        return job

    def find_by_idempotency_key(self, idempotency_key: str) -> dict | None:
        for job in self.jobs:
            if job["idempotency_key"] == idempotency_key:
                return job
        return None
