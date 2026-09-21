from app.models import IncidentResponse


class IncidentRepository:
    def __init__(self):
        self._incidents: dict[int, IncidentResponse] = {}
        self._next_id = 1
    
    def save(
        self,
        title: str,
        description: str,
        reporter: str,
        status: str,
    ) -> IncidentResponse:

        incident = IncidentResponse(
            id=self._next_id,
            title=title,
            description=description,
            reporter=reporter,
            status=status,
        )

        self._incidents[self._next_id] = incident
        self._next_id += 1

        return incident

    def get(self, incident_id: int) -> IncidentResponse | None:
        return self._incidents.get(incident_id)