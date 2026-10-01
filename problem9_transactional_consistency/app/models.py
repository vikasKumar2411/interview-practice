from pydantic import BaseModel


class OrderRequest(BaseModel):
    customer_id: int
    item: str


class OrderResponse(BaseModel):
    order_id: int
    customer_id: int
    item: str
