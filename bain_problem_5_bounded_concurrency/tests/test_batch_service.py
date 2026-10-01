import asyncio
from unittest.mock import AsyncMock

import pytest

from app.clients.ai_client import AIClient
from app.services.batch_service import BatchService


@pytest.mark.asyncio
async def test_process_items_returns_results_in_input_order():
    client = AsyncMock(spec=AIClient)
    client.process.side_effect = ["A", "B", "C"]

    service = BatchService(client)

    result = await service.process_items(["a", "b", "c"])

    assert result == [
        {"item": "a", "result": "A", "error": None},
        {"item": "b", "result": "B", "error": None},
        {"item": "c", "result": "C", "error": None},
    ]


@pytest.mark.asyncio
async def test_process_items_limits_concurrent_provider_calls_to_three():
    client = AsyncMock(spec=AIClient)
    release = asyncio.Event()
    three_started = asyncio.Event()
    active = 0
    peak = 0
    started = []

    async def process(item: str) -> str:
        nonlocal active, peak
        active += 1
        peak = max(peak, active)
        started.append(item)
        if active == 3:
            three_started.set()
        await release.wait()
        active -= 1
        return item.upper()

    client.process.side_effect = process
    service = BatchService(client)
    task = asyncio.create_task(service.process_items(["a", "b", "c", "d", "e"]))

    try:
        await asyncio.wait_for(three_started.wait(), timeout=5)
        assert active == 3
        assert len(started) == 3
    finally:
        release.set()
        await task

    assert peak == 3
    assert client.process.await_count == 5


@pytest.mark.asyncio
async def test_process_items_preserves_order_and_continues_after_failure():
    client = AsyncMock(spec=AIClient)
    gates = {item: asyncio.Event() for item in ("a", "b", "c")}
    finished = {item: asyncio.Event() for item in gates}
    all_started = asyncio.Event()
    started = []
    completion_order = []

    async def process(item: str) -> str:
        started.append(item)
        if len(started) == 3:
            all_started.set()
        await gates[item].wait()
        completion_order.append(item)
        finished[item].set()
        if item == "b":
            raise ValueError("provider failed")
        return item.upper()

    client.process.side_effect = process
    service = BatchService(client)
    task = asyncio.create_task(service.process_items(["a", "b", "c"]))

    await asyncio.wait_for(all_started.wait(), timeout=5)
    for item in ("c", "b", "a"):
        gates[item].set()
        await asyncio.wait_for(finished[item].wait(), timeout=5)

    result = await task

    assert completion_order == ["c", "b", "a"]
    assert len(result) == 3
    assert result == [
        {"item": "a", "result": "A", "error": None},
        {"item": "b", "result": None, "error": "provider failed"},
        {"item": "c", "result": "C", "error": None},
    ]
