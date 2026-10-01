from unittest.mock import AsyncMock

import pytest

from app.repositories.order_repository import OrderRepository
from app.services.order_service import OrderService


@pytest.mark.asyncio
async def test_create_order_writes_order_then_audit_event() -> None:
    repository = AsyncMock(spec=OrderRepository)
    repository.create_order.return_value = {
        "order_id": 10,
        "customer_id": 7,
        "item": "keyboard",
    }

    service = OrderService(repository)

    result = await service.create_order(
        customer_id=7,
        item="keyboard",
    )

    assert result == {
        "order_id": 10,
        "customer_id": 7,
        "item": "keyboard",
    }
    repository.create_order.assert_awaited_once_with(
        7,
        "keyboard",
    )
    repository.create_audit_event.assert_awaited_once_with(
        10,
        "order_created",
    )
