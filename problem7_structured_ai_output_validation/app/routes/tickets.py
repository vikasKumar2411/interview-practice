from fastapi import APIRouter

from app.models import TicketClassification, TicketRequest
from app.providers.ai_classifier import AIClassifier
from app.services.ticket_service import TicketService


router = APIRouter()

classifier = AIClassifier()
service = TicketService(classifier)


@router.post(
    "/tickets/classify",
    response_model=TicketClassification,
)
async def classify_ticket(request: TicketRequest) -> TicketClassification:
    result = await service.classify_ticket(request.text)
    return TicketClassification(**result)
