import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager


class OrderRepository:
    def __init__(self) -> None:
        self.orders: dict[int, dict] = {}
        self.audit_events: list[dict] = []
        self._next_order_id = 1
        self._transaction_lock = asyncio.Lock()

    @asynccontextmanager
    async def transaction(self) -> AsyncIterator[None]:
        async with self._transaction_lock:
            orders = self.orders.copy()
            audit_events = self.audit_events.copy()
            next_order_id = self._next_order_id
            try:
                yield
            except BaseException:
                self.orders.clear()
                self.orders.update(orders)
                self.audit_events[:] = audit_events
                self._next_order_id = next_order_id
                raise

    async def create_order(
        self,
        customer_id: int,
        item: str,
    ) -> dict:
        order = {
            "order_id": self._next_order_id,
            "customer_id": customer_id,
            "item": item,
        }
        self.orders[self._next_order_id] = order
        self._next_order_id += 1
        return dict(order)

    async def create_audit_event(
        self,
        order_id: int,
        event_type: str,
    ) -> None:
        self.audit_events.append(
            {
                "order_id": order_id,
                "event_type": event_type,
            }
        )
