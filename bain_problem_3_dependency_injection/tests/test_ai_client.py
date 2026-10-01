import pytest

from app.clients.ai_client import AIClient

@pytest.mark.asyncio
async def test_recommend():
    client = AIClient()

    result = await client.recommend(
        {
            "user_id": 42,
            "segment": "premium",
            "interests": ["ai"],
        }
    )

    assert result == "Recommended content for premium user"
