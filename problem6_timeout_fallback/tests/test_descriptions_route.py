from unittest.mock import AsyncMock

from fastapi.testclient import TestClient

from app.main import app
from app.routes import descriptions


client = TestClient(app)


def test_create_description_returns_description() -> None:
    response = client.post(
        "/descriptions",
        json={
            "product_name": "Travel Mug",
            "features": ["leakproof lid", "insulated"],
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "description": "Travel Mug: leakproof lid, insulated"
    }


def test_primary_non_timeout_exception_returns_server_error(monkeypatch) -> None:
    primary_call = AsyncMock(side_effect=ValueError("primary failed"))
    fallback_call = AsyncMock()
    monkeypatch.setattr(descriptions.primary_provider, "generate_description", primary_call)
    monkeypatch.setattr(descriptions.fallback_provider, "generate_description", fallback_call)

    with TestClient(app, raise_server_exceptions=False) as error_client:
        response = error_client.post(
            "/descriptions",
            json={"product_name": "Travel Mug", "features": ["insulated"]},
        )

    assert response.status_code == 500
    primary_call.assert_awaited_once_with("Travel Mug", ["insulated"])
    fallback_call.assert_not_awaited()
