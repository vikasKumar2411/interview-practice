from fastapi.testclient import TestClient

from app.api import routes
from app.main import app

client = TestClient(app)

def test_recommend_returns_200(monkeypatch):
    async def fake_recommend(user_id: int) -> str:
        return "test recommendation"

    monkeypatch.setattr(routes.service, "recommend", fake_recommend)

    response = client.post(
        "/recommend",
        json={"user_id": 42},
    )

    assert response.status_code == 200
    assert response.json() == {"recommendation": "test recommendation"}
