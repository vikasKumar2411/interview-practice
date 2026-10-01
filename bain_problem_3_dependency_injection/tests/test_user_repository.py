from app.repositories.user_repository import UserRepository

def test_get_profile():
    repo = UserRepository()
    result = repo.get_profile(42)

    assert result["user_id"] == 42
    assert result["segment"] == "premium"
