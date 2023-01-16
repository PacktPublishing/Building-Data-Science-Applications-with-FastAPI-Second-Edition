import asyncio
from pathlib import Path

import httpx
import pytest
from fastapi import status
from httpx_ws import aconnect_ws

from chapter13.chapter13_api import app as chapter13_api_app
from chapter13.websocket_object_detection.app import (
    app as chapter13_websocket_object_detection_app,
)

coffee_shop_image_file = Path(__file__).parent.parent / "assets" / "coffee-shop.jpg"
detected_labels = {"person", "couch", "chair", "laptop", "dining table"}


@pytest.mark.fastapi(app=chapter13_api_app)
@pytest.mark.asyncio
class TestChapter13API:
    async def test_invalid_payload(self, client: httpx.AsyncClient):
        response = await client.post("/object-detection", files={})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_valid_payload(self, client: httpx.AsyncClient):
        response = await client.post(
            "/object-detection", files={"image": open(coffee_shop_image_file, "rb")}
        )

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        objects = json["objects"]
        assert len(objects) > 0
        for object in objects:
            assert "box" in object
            assert object["label"] in detected_labels


@pytest.mark.fastapi(app=chapter13_websocket_object_detection_app)
@pytest.mark.asyncio
class TestChapter13WebSocketobjectDetection:
    async def test_single_detection(self, client: httpx.AsyncClient):
        async with aconnect_ws("/object-detection", client) as websocket:
            with open(coffee_shop_image_file, "rb") as image:
                await websocket.send_bytes(image.read())
                result = await websocket.receive_json()
                objects = result["objects"]
                assert len(objects) > 0
                for object in objects:
                    assert "box" in object
                    assert object["label"] in detected_labels

    async def test_backpressure(self, client: httpx.AsyncClient):
        QUEUE_LIMIT = 10
        async with aconnect_ws("/object-detection", client) as websocket:
            with open(coffee_shop_image_file, "rb") as image:
                bytes = image.read()
                for _ in range(QUEUE_LIMIT + 1):
                    await websocket.send_bytes(bytes)
                result = await websocket.receive_json()
                assert result is not None
                with pytest.raises(asyncio.TimeoutError):
                    await websocket.receive_json(timeout=0.1)
