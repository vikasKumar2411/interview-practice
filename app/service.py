from app.models import IncidentRequest, IncidentResponse
from app.repository import IncidentRepository

class Processor:
    def __init__(self):
        self.repository = IncidentRepository()

    def process_incident(self, req):
        return self.repository.save(
            title=req.title,
            description=req.description,
            reporter=req.reporter,
            status="open",
        )

    def get_incidents(self, req):
        return self.repository.get(req.incident_id)