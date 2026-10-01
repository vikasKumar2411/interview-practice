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
