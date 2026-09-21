from fastapi import APIRouter, HTTPException, status

from app.classifier import TicketClassifier
from app.models import TicketCreate, TicketResponse
from app.repository import TicketRepository
from app.service import TicketService


router = APIRouter()

repository = TicketRepository()

service = TicketService(
    repository=repository,
    classifier=TicketClassifier(),
)


@router.post(
    "/tickets",
    response_model=TicketResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_ticket(
    payload: TicketCreate,
) -> TicketResponse:

    ticket = service.create_ticket(payload)

    if ticket.confidence < 0.80:
        ticket.status = "needs_review"

    return ticket


@router.get(
    "/tickets/{ticket_id}",
    response_model=TicketResponse,
)
def get_ticket(
    ticket_id: int,
) -> TicketResponse:

    ticket = service.get_ticket(ticket_id)

    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    return ticket