from app.repositories.order_repository import OrderRepository


class OrderService:
    def __init__(self, repository: OrderRepository) -> None:
        self.repository = repository

    async def create_order(
        self,
        customer_id: int,
        item: str,
    ) -> dict:
        order = await self.repository.create_order(
            customer_id,
            item,
        )

        await self.repository.create_audit_event(
            order["order_id"],
            "order_created",
        )

        return order
