import pytest

from app.clients.ai_client import AIClient


@pytest.mark.asyncio
async def test_process():
    client = AIClient()

    result = await client.process("hello")

    assert result == "HELLO"
