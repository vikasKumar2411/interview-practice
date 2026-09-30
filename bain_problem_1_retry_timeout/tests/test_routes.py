from fastapi.testclient import TestClient

from app.errors import ClassificationUnavailableError
from app.main import app
from app.api import routes

client = TestClient(app)

def test_classify_returns_200(monkeypatch):
    async def fake_classify(text: str) -> str:
        return "cat"

    monkeypatch.setattr(routes.service, "classify", fake_classify)

    response = client.post(
        "/classify",
        json={"text": "some text"},
    )

    assert response.status_code == 200
    assert response.json() == {"label": "cat"}

def test_classification_unavailable_returns_503(monkeypatch):
    async def fake_classify(text: str) -> str:
        raise ClassificationUnavailableError("provider unavailable")

    monkeypatch.setattr(routes.service, "classify", fake_classify)

    response = client.post(
        "/classify",
        json={"text": "some text"},
    )

    assert response.status_code == 503
    assert response.json() == {"detail": "classification unavailable"}
