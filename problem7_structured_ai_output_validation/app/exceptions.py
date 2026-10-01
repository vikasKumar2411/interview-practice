from typing import Any


class InvalidAIResponseError(Exception):
    def __init__(self, payload: Any) -> None:
        self.payload = payload
        super().__init__("AI provider returned an invalid response")
