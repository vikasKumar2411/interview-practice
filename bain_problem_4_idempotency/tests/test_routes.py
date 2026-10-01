from fastapi.testclient import TestClient

from app.api import routes
from app.main import app
from app.repositories.job_repository import JobRepository
from app.services.job_service import JobService

client = TestClient(app)

def test_create_job_returns_200(monkeypatch):
    def fake_create_job(idempotency_key: str, payload: str) -> dict:
        return {
            "job_id": 7,
            "idempotency_key": idempotency_key,
            "payload": payload,
            "status": "created",
        }

    monkeypatch.setattr(routes.service, "create_job", fake_create_job)

    response = client.post(
        "/jobs",
        json={
            "idempotency_key": "abc-123",
            "payload": "hello",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "job_id": 7,
        "status": "created",
    }


def test_create_job_reuses_job_for_duplicate_key(monkeypatch):
    repository = JobRepository()
    monkeypatch.setattr(routes, "service", JobService(repository))

    first_response = client.post(
        "/jobs",
        json={"idempotency_key": "abc-123", "payload": "hello"},
    )
    duplicate_response = client.post(
        "/jobs",
        json={"idempotency_key": "abc-123", "payload": "different payload"},
    )

    assert first_response.status_code == 200
    assert first_response.json() == {"job_id": 1, "status": "created"}
    assert duplicate_response.status_code == 200
    assert duplicate_response.json() == first_response.json()
    assert len(repository.jobs) == 1
    assert repository.jobs[0]["payload"] == "hello"
