from typing import Literal

from pydantic import BaseModel, Field


class TicketCreate(BaseModel):
    customer_id: str
    message: str = Field(min_length=1)
    customer_tier: Literal["standard", "premium"] = "standard"


class TicketResponse(BaseModel):
    id: int
    customer_id: str
    message: str
    customer_tier: Literal["standard", "premium"]
    category: str
    confidence: float
    status: str