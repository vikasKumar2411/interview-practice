import asyncio
from unittest.mock import AsyncMock

import pytest

from app.repositories.order_repository import OrderRepository
from app.services.order_service import OrderService


@pytest.mark.asyncio
async def test_create_order_writes_order_then_audit_event() -> None:
    repository = OrderRepository()
    service = OrderService(repository)
    calls = []
    create_order = repository.create_order
    create_audit_event = repository.create_audit_event

    async def record_order(customer_id: int, item: str) -> dict:
        calls.append(("create_order", customer_id, item))
        return await create_order(customer_id, item)

    async def record_audit(order_id: int, event_type: str) -> None:
        calls.append(("create_audit_event", order_id, event_type))
        await create_audit_event(order_id, event_type)

    repository.create_order = record_order
    repository.create_audit_event = record_audit

    result = await service.create_order(customer_id=7, item="keyboard")

    assert result == {"order_id": 1, "customer_id": 7, "item": "keyboard"}
    assert calls == [
        ("create_order", 7, "keyboard"),
        ("create_audit_event", 1, "order_created"),
    ]
    assert repository.orders == {1: result}
    assert repository.audit_events == [
        {"order_id": 1, "event_type": "order_created"}
    ]


@pytest.mark.asyncio
async def test_order_failure_rolls_back_and_skips_audit() -> None:
    repository = OrderRepository()
    service = OrderService(repository)
    await service.create_order(7, "keyboard")
    original_create_order = repository.create_order
    original_create_audit_event = repository.create_audit_event
    before_orders = repository.orders.copy()
    before_audit_events = repository.audit_events.copy()
    before_next_order_id = repository._next_order_id
    failure = RuntimeError("order write failed")

    async def fail_after_order_write(customer_id: int, item: str) -> None:
        await original_create_order(customer_id, item)
        raise failure

    repository.create_order = AsyncMock(side_effect=fail_after_order_write)
    repository.create_audit_event = AsyncMock(wraps=original_create_audit_event)

    with pytest.raises(RuntimeError) as raised:
        await service.create_order(8, "monitor")

    assert raised.value is failure
    repository.create_audit_event.assert_not_awaited()
    assert repository.orders == before_orders
    assert repository.audit_events == before_audit_events
    assert repository._next_order_id == before_next_order_id


@pytest.mark.asyncio
async def test_audit_failure_rolls_back_order_and_audit_state() -> None:
    repository = OrderRepository()
    service = OrderService(repository)
    await service.create_order(7, "keyboard")
    original_create_audit_event = repository.create_audit_event
    before_orders = repository.orders.copy()
    before_audit_events = repository.audit_events.copy()
    before_next_order_id = repository._next_order_id
    failure = RuntimeError("audit write failed")

    async def fail_after_audit_write(order_id: int, event_type: str) -> None:
        await original_create_audit_event(order_id, event_type)
        raise failure

    repository.create_audit_event = AsyncMock(side_effect=fail_after_audit_write)

    with pytest.raises(RuntimeError) as raised:
        await service.create_order(8, "monitor")

    assert raised.value is failure
    repository.create_audit_event.assert_awaited_once_with(2, "order_created")
    assert repository.orders == before_orders
    assert repository.audit_events == before_audit_events
    assert repository._next_order_id == before_next_order_id


@pytest.mark.asyncio
async def test_failed_transaction_does_not_erase_overlapping_success() -> None:
    repository = OrderRepository()
    service = OrderService(repository)
    original_create_audit_event = repository.create_audit_event
    first_audit_started = asyncio.Event()
    release_first_audit = asyncio.Event()
    failure = RuntimeError("audit write failed")

    async def fail_first_audit(order_id: int, event_type: str) -> None:
        if not first_audit_started.is_set():
            first_audit_started.set()
            await release_first_audit.wait()
            raise failure
        await original_create_audit_event(order_id, event_type)

    repository.create_audit_event = fail_first_audit
    first = asyncio.create_task(service.create_order(7, "keyboard"))
    await first_audit_started.wait()
    second = asyncio.create_task(service.create_order(8, "monitor"))
    await asyncio.sleep(0)
    assert not second.done()

    release_first_audit.set()
    with pytest.raises(RuntimeError) as raised:
        await first
    result = await second

    assert raised.value is failure
    assert result == {"order_id": 1, "customer_id": 8, "item": "monitor"}
    assert repository.orders == {1: result}
    assert repository.audit_events == [
        {"order_id": 1, "event_type": "order_created"}
    ]
