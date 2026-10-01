from unittest.mock import AsyncMock

from fastapi.testclient import TestClient

from app.api import routes
from app.clients.ai_client import AIClient
from app.main import app


client = TestClient(app)


def test_batch_returns_200(monkeypatch):
    async def fake_process_items(items: list[str]) -> list[dict]:
        return [
            {"item": item, "result": item.upper(), "error": None}
            for item in items
        ]

    monkeypatch.setattr(routes.service, "process_items", fake_process_items)

    response = client.post(
        "/batch",
        json={"items": ["a", "b"]},
    )

    assert response.status_code == 200
    assert response.json() == {
        "results": [
            {"item": "a", "result": "A", "error": None},
            {"item": "b", "result": "B", "error": None},
        ]
    }


def test_batch_returns_partial_failure_in_input_order(monkeypatch):
    provider = AsyncMock(spec=AIClient)

    async def process(item: str) -> str:
        if item == "b":
            raise ValueError("provider failed")
        return item.upper()

    provider.process.side_effect = process
    monkeypatch.setattr(routes.service, "client", provider)

    response = client.post("/batch", json={"items": ["a", "b", "c"]})

    assert response.status_code == 200
    assert response.json() == {
        "results": [
            {"item": "a", "result": "A", "error": None},
            {"item": "b", "result": None, "error": "provider failed"},
            {"item": "c", "result": "C", "error": None},
        ]
    }
