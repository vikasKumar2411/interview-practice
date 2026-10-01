from fastapi import APIRouter, HTTPException

from app.exceptions import InvalidAIResponseError
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
    try:
        result = await service.classify_ticket(request.text)
    except InvalidAIResponseError as exc:
        raise HTTPException(
            status_code=502,
            detail="AI provider returned an invalid response",
        ) from exc
    return TicketClassification(**result)
