from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_order_returns_created_order() -> None:
    response = client.post(
        "/orders",
        json={
            "customer_id": 42,
            "item": "monitor",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "order_id": 1,
        "customer_id": 42,
        "item": "monitor",
    }
