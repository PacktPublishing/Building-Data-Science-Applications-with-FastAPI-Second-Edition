import httpx
import pytest
from fastapi import status

from chapter07.chapter07_api_key_header import (
    API_TOKEN as CHAPTER07_API_KEY_HEADER_API_TOKEN,
)
from chapter07.chapter07_api_key_header import app as chapter07_api_key_header_app
from chapter07.chapter07_api_key_header_dependency import (
    API_TOKEN as CHAPTER07_API_KEY_HEADER_DEPENDENCY_API_TOKEN,
)
from chapter07.chapter07_api_key_header_dependency import (
    app as chapter07_api_key_header_app_dependency,
)


@pytest.mark.fastapi(app=chapter07_api_key_header_app)
@pytest.mark.asyncio
class TestChapter07APIKeyHeader:
    async def test_missing_header(self, client: httpx.AsyncClient):
        response = await client.get("/protected-route")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_invalid_token(self, client: httpx.AsyncClient):
        response = await client.get("/protected-route", headers={"Token": "Foo"})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_valid_token(self, client: httpx.AsyncClient):
        response = await client.get(
            "/protected-route", headers={"Token": CHAPTER07_API_KEY_HEADER_API_TOKEN}
        )

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == {"hello": "world"}


@pytest.mark.fastapi(app=chapter07_api_key_header_app_dependency)
@pytest.mark.asyncio
class TestChapter07APIKeyHeaderDependency:
    async def test_missing_header(self, client: httpx.AsyncClient):
        response = await client.get("/protected-route")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_invalid_token(self, client: httpx.AsyncClient):
        response = await client.get("/protected-route", headers={"Token": "Foo"})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_valid_token(self, client: httpx.AsyncClient):
        response = await client.get(
            "/protected-route",
            headers={"Token": CHAPTER07_API_KEY_HEADER_DEPENDENCY_API_TOKEN},
        )

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert json == {"hello": "world"}
