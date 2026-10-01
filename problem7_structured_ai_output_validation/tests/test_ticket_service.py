from unittest.mock import AsyncMock

import pytest

from app.exceptions import InvalidAIResponseError
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


@pytest.mark.asyncio
async def test_classify_ticket_ignores_extra_provider_fields() -> None:
    classifier = AsyncMock(spec=AIClassifier)
    classifier.classify.return_value = {
        "category": "billing",
        "priority": "high",
        "summary": "Customer was charged twice",
        "provider_metadata": "internal",
    }

    result = await TicketService(classifier).classify_ticket("I was charged twice")

    assert result == {
        "category": "billing",
        "priority": "high",
        "summary": "Customer was charged twice",
    }
    classifier.classify.assert_awaited_once_with("I was charged twice")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload",
    [
        {"category": "other", "priority": "high", "summary": "Issue"},
        {"category": "billing", "priority": "urgent", "summary": "Issue"},
        {"category": "billing", "priority": "high"},
        {"category": "billing", "priority": "high", "summary": ""},
    ],
    ids=["invalid-category", "invalid-priority", "missing-summary", "empty-summary"],
)
async def test_classify_ticket_rejects_invalid_provider_response(payload: dict) -> None:
    classifier = AsyncMock(spec=AIClassifier)
    classifier.classify.return_value = payload

    with pytest.raises(InvalidAIResponseError) as error:
        await TicketService(classifier).classify_ticket("Issue")

    assert error.value.payload is payload
    classifier.classify.assert_awaited_once_with("Issue")


@pytest.mark.asyncio
async def test_classify_ticket_preserves_unrelated_provider_exception() -> None:
    classifier = AsyncMock(spec=AIClassifier)
    provider_error = RuntimeError("provider unavailable")
    classifier.classify.side_effect = provider_error

    with pytest.raises(RuntimeError) as error:
        await TicketService(classifier).classify_ticket("Issue")

    assert error.value is provider_error
    classifier.classify.assert_awaited_once_with("Issue")
