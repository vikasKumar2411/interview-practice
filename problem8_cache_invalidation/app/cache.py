class RecommendationCache:
    def __init__(self) -> None:
        self._values: dict[int, str] = {}

    def get(self, user_id: int) -> str | None:
        return self._values.get(user_id)

    def set(self, user_id: int, recommendation: str) -> None:
        self._values[user_id] = recommendation
