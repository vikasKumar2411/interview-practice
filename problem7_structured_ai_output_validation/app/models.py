from typing import Literal

from pydantic import BaseModel


class TicketRequest(BaseModel):
    text: str


class TicketClassification(BaseModel):
    category: Literal["billing", "technical", "account"]
    priority: Literal["low", "medium", "high"]
    summary: str
