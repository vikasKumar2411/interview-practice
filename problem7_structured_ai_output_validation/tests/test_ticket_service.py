from unittest.mock import AsyncMock

import pytest

from app.providers.ai_classifier import AIClassifier
from app.services.ticket_service import TicketService


@pytest.mark.asyncio
async def test_classify_ticket_returns_provider_result() -> None:
    classifier = AsyncMock(spec=AIClassifier)
    classifier.classify.return_value = {
        "category": "billing",
        "priority": "high",
        "summary": "Customer was charged twice",
    }

    service = TicketService(classifier)

    result = await service.classify_ticket("I was charged twice")

    assert result == {
        "category": "billing",
        "priority": "high",
        "summary": "Customer was charged twice",
    }
    classifier.classify.assert_awaited_once_with("I was charged twice")
