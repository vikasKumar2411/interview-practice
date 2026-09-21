from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_review():
    response = client.post(
        "/reviews",
        json={
            "document_name": "contract.pdf",
            "submitted_by": "user@example.com",
            "priority": "normal",
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["document_name"] == "contract.pdf"
    assert body["submitted_by"] == "user@example.com"
    assert body["priority"] == "normal"
    assert body["status"] == "pending"


def test_get_missing_review_returns_404():
    response = client.get("/reviews/999")

    assert response.status_code == 404


def test_invalid_email_returns_422():
    response = client.post(
        "/reviews",
        json={
            "document_name": "contract.pdf",
            "submitted_by": "not-an-email",
            "priority": "normal",
        },
    )

    assert response.status_code == 422


def test_invalid_priority_returns_422():
    response = client.post(
        "/reviews",
        json={
            "document_name": "contract.pdf",
            "submitted_by": "user@example.com",
            "priority": "urgent",
        },
    )

    assert response.status_code == 422