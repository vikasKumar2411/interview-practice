import asyncio

import httpx
import pytest
from unittest.mock import AsyncMock

from app.errors import ClassificationUnavailableError
from app.services.classification import ClassificationService

@pytest.mark.asyncio
async def test_classify_returns_client_result():
    client = AsyncMock()
    client.classify.return_value = "cat"

    service = ClassificationService(client)

    result = await service.classify("some text")

    assert result == "cat"
    client.classify.assert_awaited_once_with("some text")

@pytest.mark.asyncio
async def test_timeout_then_success_retries_once():
    attempts = 0

    async def classify(text):
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            await asyncio.Event().wait()
        return "cat"

    client = AsyncMock()
    client.classify.side_effect = classify

    result = await asyncio.wait_for(
        ClassificationService(client).classify("some text"), timeout=3.0
    )

    assert result == "cat"
    assert client.classify.await_count == 2
    client.classify.assert_any_await("some text")

@pytest.mark.asyncio
async def test_two_timeouts_raise_unavailable():
    first_timeout = httpx.ReadTimeout("first attempt")
    second_timeout = httpx.ReadTimeout("second attempt")
    client = AsyncMock()
    client.classify.side_effect = [first_timeout, second_timeout]

    with pytest.raises(ClassificationUnavailableError) as error:
        await ClassificationService(client).classify("some text")

    assert error.value.__cause__ is second_timeout
    assert client.classify.await_count == 2

@pytest.mark.asyncio
async def test_non_timeout_exception_propagates():
    client = AsyncMock()
    client.classify.side_effect = ValueError("bad provider response")

    service = ClassificationService(client)

    with pytest.raises(ValueError, match="bad provider response"):
        await service.classify("some text")

    client.classify.assert_awaited_once_with("some text")

@pytest.mark.asyncio
async def test_non_timeout_exception_after_timeout_propagates():
    error = ValueError("bad provider response")
    client = AsyncMock()
    client.classify.side_effect = [httpx.ReadTimeout("first attempt"), error]

    with pytest.raises(ValueError) as raised:
        await ClassificationService(client).classify("some text")

    assert raised.value is error
    assert client.classify.await_count == 2
