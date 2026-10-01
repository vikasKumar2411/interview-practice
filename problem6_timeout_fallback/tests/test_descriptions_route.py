from fastapi.testclient import TestClient

from app.main import app


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
