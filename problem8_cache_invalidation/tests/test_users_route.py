from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_update_user_returns_updated_interests() -> None:
    response = client.put(
        "/users/1",
        json={"interests": ["agentic ai", "testing"]},
    )

    assert response.status_code == 200
    assert response.json() == {
        "user_id": 1,
        "interests": ["agentic ai", "testing"],
    }
