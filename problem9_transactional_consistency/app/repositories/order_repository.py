class OrderRepository:
    def __init__(self) -> None:
        self.orders: dict[int, dict] = {}
        self.audit_events: list[dict] = []
        self._next_order_id = 1

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
