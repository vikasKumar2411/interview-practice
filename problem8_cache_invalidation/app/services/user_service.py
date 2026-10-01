from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def update_interests(
        self,
        user_id: int,
        interests: list[str],
    ) -> list[str]:
        return await self.repository.update_interests(user_id, interests)
