from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_classify_ticket_returns_classification() -> None:
    response = client.post(
        "/tickets/classify",
        json={"text": "My password reset link does not work"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "category": "technical",
        "priority": "medium",
        "summary": "Technical issue: My password reset link does not work",
    }
