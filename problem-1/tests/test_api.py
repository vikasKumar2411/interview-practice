from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_billing_ticket():
    response = client.post(
        "/tickets",
        json={
            "customer_id": "customer-100",
            "message": "I was charged twice",
            "customer_tier": "standard",
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["category"] == "billing"
    assert body["status"] == "new"


def test_low_confidence_ticket_requires_review():
    response = client.post(
        "/tickets",
        json={
            "customer_id": "customer-101",
            "message": "Something unusual happened",
            "customer_tier": "standard",
        },
    )

    assert response.status_code == 201
    assert response.json()["status"] == "needs_review"


def test_missing_ticket_returns_404():
    response = client.get("/tickets/9999")

    assert response.status_code == 404