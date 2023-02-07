import uuid
from typing import Any
from unittest.mock import MagicMock, patch

import httpx
import pytest
from dramatiq import Message
from fastapi import status
from PIL import Image

from chapter14.basic.api import app as chapter14_app
from chapter14.basic.text_to_image import TextToImage
from chapter14.basic.worker import text_to_image_task


def test_chapter14_basic_text_to_image():
    text_to_image = TextToImage()
    text_to_image.load_model()
    image = text_to_image.generate(
        "a photo of squirrels partying in a night club", num_steps=1
    )
    assert isinstance(image, Image.Image)


@pytest.mark.fastapi(app=chapter14_app)
@pytest.mark.asyncio
class TestChapter14BasicAPI:
    @pytest.mark.parametrize(
        "payload",
        [
            {},
            {"prompt": "PROMPT", "num_steps": -1},
            {"prompt": "PROMPT", "num_steps": 0},
            {"prompt": "PROMPT", "num_steps": 100},
        ],
    )
    async def test_invalid_payload(
        self, payload: dict[str, Any], client: httpx.AsyncClient
    ):
        response = await client.post("/image-generation", json=payload)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_valid(self, client: httpx.AsyncClient):
        message_mock = MagicMock(spec=Message)
        message_mock.message_id = str(uuid.uuid4())

        with patch.object(
            text_to_image_task, "send", return_value=message_mock
        ) as send_mock:
            response = await client.post("/image-generation", json={"prompt": "PROMPT"})

            assert response.status_code == status.HTTP_202_ACCEPTED
            json = response.json()
            assert json["task_id"] == message_mock.message_id

            send_mock.assert_called_once_with(
                "PROMPT", negative_prompt=None, num_steps=50
            )
