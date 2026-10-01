from pydantic import BaseModel


class DescriptionRequest(BaseModel):
    product_name: str
    features: list[str]


class DescriptionResponse(BaseModel):
    description: str
