from fastapi import APIRouter, HTTPException, status

from app.models import IncidentRequest, IncidentResponse
from app.service import Processor


router = APIRouter()
processor = Processor()


@router.post(
    "/incidents",
    response_model=IncidentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_incident(
    req: IncidentRequest,
) -> IncidentResponse:
    return processor.process_incident(req)


@router.get(
    "/incidents/{incident_id}",
    response_model=IncidentResponse,
)
def get_incident(
    incident_id: int,
) -> IncidentResponse:

    incident = processor.get_incident(incident_id)

    if incident is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incident not found",
        )

    return incident