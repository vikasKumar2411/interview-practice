import pytest
import httpx

from app.clients.ai_client import AIClient

@pytest.mark.asyncio
async def test_ai_client_classify(monkeypatch):
    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {"label": "cat"}
    
    class FakeAsyncClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            pass

        async def post(self, url, json):
            return FakeResponse()

    monkeypatch.setattr(httpx, "AsyncClient", FakeAsyncClient)

    client = AIClient(base_url="https://example.test")
    result = await client.classify("some text")

    assert result == "cat"
