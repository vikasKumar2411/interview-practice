from app.classifier import TicketClassifier
from app.models import TicketCreate, TicketResponse
from app.repository import TicketRepository


class TicketService:
    def __init__(
        self,
        repository: TicketRepository,
        classifier: TicketClassifier,
    ):
        self.repository = repository
        self.classifier = classifier

    def create_ticket(
        self,
        payload: TicketCreate,
    ) -> TicketResponse:

        category, confidence = self.classifier.classify(
            payload.message
        )

        ticket = TicketResponse(
            id=0,
            customer_id=payload.customer_id,
            message=payload.message,
            customer_tier=payload.customer_tier,
            category=category,
            confidence=confidence,
            status="new",
        )

        return self.repository.save(ticket)

    def get_ticket(
        self,
        ticket_id: int,
    ) -> TicketResponse | None:
        return self.repository.get(ticket_id)