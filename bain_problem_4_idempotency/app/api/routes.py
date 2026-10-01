from fastapi import APIRouter

from app.models.job import JobRequest, JobResponse
from app.repositories.job_repository import JobRepository
from app.services.job_service import JobService

router = APIRouter()
repository = JobRepository()
service = JobService(repository)

@router.post("/jobs", response_model=JobResponse)
def create_job(request: JobRequest):
    job = service.create_job(
        request.idempotency_key,
        request.payload,
    )
    return JobResponse(
        job_id=job["job_id"],
        status=job["status"],
    )
