import asyncio
from unittest.mock import AsyncMock

import pytest

from app.providers.primary_ai import PrimaryAIProvider
from app.providers.fallback_ai import FallbackAIProvider
from app.services.description_service import DescriptionService


@pytest.mark.asyncio
async def test_generate_description_returns_primary_result() -> None:
    primary = AsyncMock(spec=PrimaryAIProvider)
    fallback = AsyncMock(spec=FallbackAIProvider)

    primary.generate_description.return_value = "primary result"

    service = DescriptionService(
        primary_provider=primary,
        fallback_provider=fallback,
    )

    result = await service.generate_description(
        "Noise-Cancelling Headphones",
        ["40-hour battery", "Bluetooth 5.3"],
    )

    assert result == "primary result"
    primary.generate_description.assert_awaited_once_with(
        "Noise-Cancelling Headphones",
        ["40-hour battery", "Bluetooth 5.3"],
    )
    fallback.generate_description.assert_not_awaited()


@pytest.mark.asyncio
async def test_primary_deadline_calls_fallback_without_fallback_timeout() -> None:
    primary = AsyncMock(spec=PrimaryAIProvider)
    fallback = AsyncMock(spec=FallbackAIProvider)

    async def slow_primary(product_name: str, features: list[str]) -> str:
        await asyncio.sleep(1)
        return "late primary result"

    async def slow_fallback(product_name: str, features: list[str]) -> str:
        await asyncio.sleep(0.25)
        return "fallback result"

    primary.generate_description.side_effect = slow_primary
    fallback.generate_description.side_effect = slow_fallback
    service = DescriptionService(primary, fallback)

    result = await service.generate_description("Travel Mug", ["insulated"])

    assert result == "fallback result"
    primary.generate_description.assert_awaited_once_with("Travel Mug", ["insulated"])
    fallback.generate_description.assert_awaited_once_with("Travel Mug", ["insulated"])


@pytest.mark.asyncio
async def test_primary_timeout_propagates_fallback_exception() -> None:
    primary = AsyncMock(spec=PrimaryAIProvider)
    fallback = AsyncMock(spec=FallbackAIProvider)
    primary.generate_description.side_effect = TimeoutError("primary timed out")
    fallback_error = RuntimeError("fallback failed")
    fallback.generate_description.side_effect = fallback_error
    service = DescriptionService(primary, fallback)

    with pytest.raises(RuntimeError) as caught:
        await service.generate_description("Travel Mug", ["insulated"])

    assert caught.value is fallback_error
    primary.generate_description.assert_awaited_once_with("Travel Mug", ["insulated"])
    fallback.generate_description.assert_awaited_once_with("Travel Mug", ["insulated"])


@pytest.mark.asyncio
async def test_primary_non_timeout_exception_skips_fallback() -> None:
    primary = AsyncMock(spec=PrimaryAIProvider)
    fallback = AsyncMock(spec=FallbackAIProvider)
    primary_error = ValueError("primary failed")
    primary.generate_description.side_effect = primary_error
    service = DescriptionService(primary, fallback)

    with pytest.raises(ValueError) as caught:
        await service.generate_description("Travel Mug", ["insulated"])

    assert caught.value is primary_error
    primary.generate_description.assert_awaited_once_with("Travel Mug", ["insulated"])
    fallback.generate_description.assert_not_awaited()
