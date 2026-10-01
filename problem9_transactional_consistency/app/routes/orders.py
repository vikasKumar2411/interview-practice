from fastapi import APIRouter

from app.models import OrderRequest, OrderResponse
from app.repositories.order_repository import OrderRepository
from app.services.order_service import OrderService


router = APIRouter()

repository = OrderRepository()
service = OrderService(repository)


@router.post(
    "/orders",
    response_model=OrderResponse,
)
async def create_order(request: OrderRequest) -> OrderResponse:
    order = await service.create_order(
        request.customer_id,
        request.item,
    )
    return OrderResponse(**order)
