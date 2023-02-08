import asyncio

import httpx
import pytest
from fastapi import status
from httpx_ws import WebSocketDisconnect, aconnect_ws

from chapter08.broadcast.app import app as chapter08_broadcast_app
from chapter08.concurrency.app import app as chapter08_concurrency_app
from chapter08.dependencies.app import API_TOKEN
from chapter08.dependencies.app import app as chapter08_dependencies_app
from chapter08.echo.app import app as chapter08_echo_app


@pytest.mark.fastapi(app=chapter08_echo_app)
@pytest.mark.asyncio
class TestChapter08Echo:
    async def test_echo(self, client: httpx.AsyncClient):
        async with aconnect_ws("/ws", client) as websocket:
            await websocket.send_text("Hello")
            await websocket.send_text("World")

            message1 = await websocket.receive_text()
            message2 = await websocket.receive_text()

            assert message1 == "Message text was: Hello"
            assert message2 == "Message text was: World"


@pytest.mark.fastapi(app=chapter08_concurrency_app)
@pytest.mark.asyncio
class TestChapter08Concurrency:
    async def test_echo(self, client: httpx.AsyncClient):
        async with aconnect_ws("/ws", client) as websocket:
            message_time = await websocket.receive_text()

            await websocket.send_text("Hello")
            message_echo = await websocket.receive_text()

            assert message_time.startswith("It is:")
            assert message_echo == "Message text was: Hello"


@pytest.mark.fastapi(app=chapter08_dependencies_app)
@pytest.mark.asyncio
class TestChapter08Dependencies:
    async def test_missing_token(self, client: httpx.AsyncClient):
        with pytest.raises(WebSocketDisconnect) as e:
            async with aconnect_ws("/ws", client) as ws:
                await ws.receive_text()
        assert e.value.code == status.WS_1008_POLICY_VIOLATION

    async def test_invalid_token(self, client: httpx.AsyncClient):
        with pytest.raises(WebSocketDisconnect) as e:
            async with aconnect_ws(
                "/ws", client, headers={"Cookie": "token=INVALID_TOKEN"}
            ) as ws:
                await ws.receive_text()
        assert e.value.code == status.WS_1008_POLICY_VIOLATION

    @pytest.mark.parametrize(
        "username,welcome_message",
        [(None, "Hello, Anonymous!"), ("John", "Hello, John!")],
    )
    async def test_valid_token(
        self, client: httpx.AsyncClient, username: str | None, welcome_message: str
    ):
        url = "/ws"
        if username:
            url += f"?username={username}"

        async with aconnect_ws(
            url, client, headers={"Cookie": f"token={API_TOKEN}"}
        ) as websocket:
            message1 = await websocket.receive_text()

            await websocket.send_text("Hello")
            message2 = await websocket.receive_text()

            assert message1 == welcome_message
            assert message2 == "Message text was: Hello"


@pytest.mark.fastapi(app=chapter08_broadcast_app)
@pytest.mark.asyncio
@pytest.mark.skip
class TestChapter08Broadcast:
    async def test_broadcast(self, client: httpx.AsyncClient):
        async with aconnect_ws("/ws?username=U1", client) as websocket1:
            async with aconnect_ws("/ws?username=U2", client) as websocket2:
                await websocket1.send_text("Hello from U1")
                await websocket2.send_text("Hello from U2")

                [websocket1_message, websocket2_message] = await asyncio.gather(
                    websocket1.receive_json(), websocket2.receive_json()
                )
                assert websocket1_message == {
                    "username": "U2",
                    "message": "Hello from U2",
                }
                assert websocket2_message == {
                    "username": "U1",
                    "message": "Hello from U1",
                }
