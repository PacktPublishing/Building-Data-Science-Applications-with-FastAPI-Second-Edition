from fastapi import Depends, FastAPI, Header, HTTPException, status
from loguru import logger


def secret_header(secret_header: str | None = Header(None)) -> None:
    logger.debug("Check secret header")
    if not secret_header or secret_header != "SECRET_VALUE":
        logger.warning("Invalid or missing secret header")
        raise HTTPException(status.HTTP_403_FORBIDDEN)


app = FastAPI(dependencies=[Depends(secret_header)])


@app.get("/route1")
async def route1():
    return {"route": "route1"}


@app.get("/route2")
async def route2():
    return {"route": "route2"}
