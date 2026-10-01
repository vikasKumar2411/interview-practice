from pydantic import BaseModel

class JobRequest(BaseModel):
    idempotency_key: str
    payload: str

class JobResponse(BaseModel):
    job_id: int
    status: str
