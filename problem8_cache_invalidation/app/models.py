from pydantic import BaseModel


class UserUpdateRequest(BaseModel):
    interests: list[str]


class UserResponse(BaseModel):
    user_id: int
    interests: list[str]


class RecommendationResponse(BaseModel):
    recommendation: str
