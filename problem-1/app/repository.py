from app.models import TicketResponse


class TicketRepository:
    def __init__(self):
        self._tickets: dict[int, TicketResponse] = {}
        self._next_id = 1

    def save(self, ticket: TicketResponse) -> TicketResponse:
        ticket.id = self._next_id
        self._tickets[self._next_id] = ticket
        self._next_id += 1

        return ticket

    def get(self, ticket_id: int) -> TicketResponse | None:
        return self._tickets.get(ticket_id)