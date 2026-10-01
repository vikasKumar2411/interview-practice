from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class TicketRequest(BaseModel):
    text: str


class TicketClassification(BaseModel):
    model_config = ConfigDict(extra="ignore")

    category: Literal["billing", "technical", "account"]
    priority: Literal["low", "medium", "high"]
    summary: str = Field(min_length=1)
