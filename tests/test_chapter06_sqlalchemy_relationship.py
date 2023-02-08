from collections.abc import AsyncGenerator
from typing import Any

import httpx
import pytest
import pytest_asyncio
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from chapter06.sqlalchemy_relationship.app import app
from chapter06.sqlalchemy_relationship.database import get_async_session
from chapter06.sqlalchemy_relationship.models import Base, Comment, Post

DATABASE_FILE_PATH = "chapter06_sqlalchemy.test.db"
DATABASE_URL = f"sqlite+aiosqlite:///{DATABASE_FILE_PATH}"
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_test_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


@pytest_asyncio.fixture(autouse=True, scope="module")
async def initialize_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    initial_posts = [
        Post(id=1, title="Post 1", content="Content 1"),
        Post(id=2, title="Post 2", content="Content 2"),
        Post(id=3, title="Post 3", content="Content 3"),
    ]

    initial_comments = [
        Comment(id=1, post=initial_posts[0], content="Post 1 Comment 1"),
        Comment(id=2, post=initial_posts[0], content="Post 1 Comment 2"),
        Comment(id=3, post=initial_posts[0], content="Post 1 Comment 3"),
    ]

    async with async_session_maker() as session:
        for post in initial_posts:
            session.add(post)
        for comment in initial_comments:
            session.add(comment)
        await session.commit()

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.mark.fastapi(
    app=app, dependency_overrides={get_async_session: get_test_async_session}
)
@pytest.mark.asyncio
class TestChapter06SQLAlchemyRelationship:
    @pytest.mark.parametrize(
        "skip,limit,nb_results", [(None, None, 3), (0, 1, 1), (10, 1, 0)]
    )
    async def test_list_posts(
        self,
        client: httpx.AsyncClient,
        skip: int | None,
        limit: int | None,
        nb_results: int,
    ):
        params = {}
        if skip:
            params["skip"] = skip
        if limit:
            params["limit"] = limit
        response = await client.get("/posts", params=params)

        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert len(json) == nb_results

    @pytest.mark.parametrize(
        "id,status_code,nb_comments",
        [(1, status.HTTP_200_OK, 3), (10, status.HTTP_404_NOT_FOUND, 0)],
    )
    async def test_get_post(
        self, client: httpx.AsyncClient, id: int, status_code: int, nb_comments: int
    ):
        response = await client.get(f"/posts/{id}")

        assert response.status_code == status_code
        if status_code == status.HTTP_200_OK:
            json = response.json()
            assert json["id"] == id
            assert len(json["comments"]) == nb_comments

    @pytest.mark.parametrize(
        "payload,status_code",
        [
            ({"title": "New post", "content": "New content"}, status.HTTP_201_CREATED),
            ({}, status.HTTP_422_UNPROCESSABLE_ENTITY),
        ],
    )
    async def test_create_post(
        self, client: httpx.AsyncClient, payload: dict[str, Any], status_code: int
    ):
        response = await client.post("/posts", json=payload)

        assert response.status_code == status_code
        if status_code == status.HTTP_201_CREATED:
            json = response.json()
            assert "id" in json
            assert json["comments"] == []

    @pytest.mark.parametrize(
        "id,payload,status_code,nb_comments",
        [
            (1, {"title": "Post 1 Updated"}, status.HTTP_200_OK, 3),
            (2, {"title": "Post 2 Updated"}, status.HTTP_200_OK, 0),
            (10, {"title": "Post 10 Updated"}, status.HTTP_404_NOT_FOUND, 0),
        ],
    )
    async def test_update_post(
        self,
        client: httpx.AsyncClient,
        id: int,
        payload: dict[str, Any],
        status_code: int,
        nb_comments: int,
    ):
        response = await client.patch(f"/posts/{id}", json=payload)

        assert response.status_code == status_code
        if status_code == status.HTTP_200_OK:
            json = response.json()
            for key in payload:
                assert json[key] == payload[key]
            assert len(json["comments"]) == nb_comments

    @pytest.mark.parametrize(
        "id,status_code",
        [(1, status.HTTP_204_NO_CONTENT), (10, status.HTTP_404_NOT_FOUND)],
    )
    async def test_delete_post(
        self, client: httpx.AsyncClient, id: int, status_code: int
    ):
        response = await client.delete(f"/posts/{id}")

        assert response.status_code == status_code

    @pytest.mark.parametrize(
        "post_id,payload,status_code",
        [
            (2, {"content": "New comment"}, status.HTTP_201_CREATED),
            (10, {"content": "New comment"}, status.HTTP_404_NOT_FOUND),
            (2, {}, status.HTTP_422_UNPROCESSABLE_ENTITY),
        ],
    )
    async def test_create_comment(
        self,
        client: httpx.AsyncClient,
        post_id: int,
        payload: dict[str, Any],
        status_code: int,
    ):
        response = await client.post(f"/posts/{post_id}/comments", json=payload)

        assert response.status_code == status_code
        if status_code == status.HTTP_201_CREATED:
            json = response.json()
            assert "id" in json
