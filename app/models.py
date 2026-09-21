from pydantic import BaseModel


class IncidentRequest(BaseModel):
    title: str
    description: str
    reporter: str
    

class IncidentResponse(BaseModel):
    id: int,
    title: str
    description: str
    reporter: str
    status: str