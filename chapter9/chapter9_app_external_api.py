from typing import Any

import httpx
from fastapi import Depends, FastAPI

app = FastAPI()


class ExternalAPI:
    def __init__(self) -> None:
        self.client = httpx.AsyncClient(
            base_url="https://dummy.restapiexample.com/api/v1/"
        )

    async def __call__(self) -> dict[str, Any]:
        async with self.client as client:
            response = await client.get("employees")
            return response.json()


external_api = ExternalAPI()


@app.get("/employees")
async def external_employees(employees: dict[str, Any] = Depends(external_api)):
    return employees
