import httpx
import pytest
from _pytest.logging import LogCaptureFixture
from fastapi import status
from loguru import logger

from chapter15.chapter15_logs_01 import is_even as chapter15_logs_01_is_even
from chapter15.chapter15_logs_02 import is_even as chapter15_logs_02_is_even
from chapter15.chapter15_logs_03 import is_even as chapter15_logs_03_is_even
from chapter15.chapter15_logs_04 import is_even as chapter15_logs_04_is_even
from chapter15.chapter15_logs_05 import app as chapter15_logs_05_app
from chapter15.chapter15_logs_06 import app as chapter15_logs_06_app


@pytest.fixture
def caplog(caplog: LogCaptureFixture):
    handler_id = logger.add(caplog.handler, format="{message}")
    yield caplog
    logger.remove(handler_id)


@pytest.mark.parametrize(
    "is_even",
    [
        chapter15_logs_01_is_even,
        chapter15_logs_02_is_even,
        chapter15_logs_03_is_even,
        chapter15_logs_04_is_even,
    ],
)
class TestChapter15LogsIsEven:
    def test_valid_integer(self, is_even, caplog: LogCaptureFixture):
        assert is_even(2)
        assert len(caplog.records) == 1

    def test_invalid_integer(self, is_even, caplog: LogCaptureFixture):
        with pytest.raises(TypeError):
            assert is_even("Invalid")
        assert len(caplog.records) == 2


@pytest.mark.parametrize(
    [],
    [
        pytest.param(
            marks=pytest.mark.fastapi(app=chapter15_logs_05_app), id="chapter15_logs_05"
        ),
        pytest.param(
            marks=pytest.mark.fastapi(app=chapter15_logs_06_app), id="chapter15_logs_06"
        ),
    ],
)
@pytest.mark.parametrize("path", ["/route1", "/route2"])
@pytest.mark.asyncio
class TestChapter15LogsApp:
    @pytest.mark.parametrize("secret_header", [None, "INVALID_VALUE"])
    async def test_invalid_header(
        self,
        client: httpx.AsyncClient,
        path: str,
        secret_header: str | None,
        caplog: LogCaptureFixture,
    ):
        headers = {}
        if secret_header:
            headers["Secret-Header"] = secret_header
        response = await client.get(path, headers=headers)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert len([r for r in caplog.records if r.module.startswith("chapter15")]) == 2

    async def test_valid_header(
        self, path: str, client: httpx.AsyncClient, caplog: LogCaptureFixture
    ):
        response = await client.get(path, headers={"Secret-Header": "SECRET_VALUE"})

        assert response.status_code == status.HTTP_200_OK
        assert len([r for r in caplog.records if r.module.startswith("chapter15")]) == 1
