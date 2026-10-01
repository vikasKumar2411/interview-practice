from unittest.mock import AsyncMock

from fastapi.testclient import TestClient

from app.main import app
from app.routes import tickets


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


def test_classify_ticket_returns_502_for_invalid_ai_response(monkeypatch) -> None:
    classify = AsyncMock(
        return_value={
            "category": "unknown",
            "priority": "medium",
            "summary": "Issue",
        }
    )
    monkeypatch.setattr(tickets.classifier, "classify", classify)

    response = client.post("/tickets/classify", json={"text": "Issue"})

    assert response.status_code == 502
    assert response.json() == {"detail": "AI provider returned an invalid response"}
    classify.assert_awaited_once_with("Issue")
