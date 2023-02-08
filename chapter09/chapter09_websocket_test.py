import asyncio

import httpx
import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from httpx_ws import aconnect_ws
from httpx_ws.transport import ASGIWebSocketTransport

from chapter09.chapter09_websocket import app


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def test_client():
    async with LifespanManager(app):
        async with httpx.AsyncClient(
            transport=ASGIWebSocketTransport(app), base_url="http://app.io"
        ) as test_client:
            yield test_client


@pytest.mark.asyncio
async def test_websocket_echo(test_client: httpx.AsyncClient):
    async with aconnect_ws("/ws", test_client) as websocket:
        await websocket.send_text("Hello")

        message = await websocket.receive_text()
        assert message == "Message text was: Hello"
