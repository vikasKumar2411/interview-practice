from app.classifier import TicketClassifier
from app.models import TicketCreate
from app.repository import TicketRepository
from app.service import TicketService


def build_service() -> TicketService:
    return TicketService(
        repository=TicketRepository(),
        classifier=TicketClassifier(),
    )


def test_security_ticket_is_classified():
    service = build_service()

    ticket = service.create_ticket(
        TicketCreate(
            customer_id="customer-1",
            message="My card was stolen",
        )
    )

    assert ticket.category == "security"
    assert ticket.confidence == 0.96


def test_billing_ticket_is_classified():
    service = build_service()

    ticket = service.create_ticket(
        TicketCreate(
            customer_id="customer-2",
            message="I was charged twice",
        )
    )

    assert ticket.category == "billing"
    assert ticket.confidence == 0.91