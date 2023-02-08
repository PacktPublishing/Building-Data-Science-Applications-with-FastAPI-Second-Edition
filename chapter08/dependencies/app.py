from fastapi import Cookie, FastAPI, WebSocket, WebSocketException, status
from starlette.websockets import WebSocketDisconnect

API_TOKEN = "SECRET_API_TOKEN"

app = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket, username: str = "Anonymous", token: str = Cookie(...)
):
    if token != API_TOKEN:
        raise WebSocketException(status.WS_1008_POLICY_VIOLATION)

    await websocket.accept()

    await websocket.send_text(f"Hello, {username}!")
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        pass
