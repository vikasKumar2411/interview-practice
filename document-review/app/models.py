from typing import Literal

from pydantic import BaseModel, EmailStr


class ReviewRequest(BaseModel):
    document_name: str
    submitted_by: EmailStr
    priority: Literal["normal", "high"] = "normal"


class ReviewResponse(BaseModel):
    id: int
    document_name: str
    submitted_by: EmailStr
    priority: Literal["normal", "high"]
    status: str