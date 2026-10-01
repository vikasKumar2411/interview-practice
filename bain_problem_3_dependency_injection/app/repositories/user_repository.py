class UserRepository:
    def get_profile(self, user_id: int) -> dict:
        return {
            "user_id": user_id,
            "segment": "premium",
            "interests": ["ai", "cloud"],
        }
