class UserRepository:
    def __init__(self) -> None:
        self._users: dict[int, list[str]] = {
            1: ["python", "distributed systems"],
            2: ["machine learning"],
        }

    async def get_interests(self, user_id: int) -> list[str]:
        return list(self._users[user_id])

    async def update_interests(
        self,
        user_id: int,
        interests: list[str],
    ) -> list[str]:
        self._users[user_id] = list(interests)
        return list(self._users[user_id])
