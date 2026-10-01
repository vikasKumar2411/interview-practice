from pydantic import BaseModel


class BatchRequest(BaseModel):
    items: list[str]


class BatchItemResult(BaseModel):
    item: str
    result: str | None = None
    error: str | None = None


class BatchResponse(BaseModel):
    results: list[BatchItemResult]
