from fastapi import Depends, FastAPI

app = FastAPI()


async def pagination(skip: int = 0, limit: int = 10) -> tuple[int, int]:
    return (skip, limit)


@app.get("/items")
async def list_items(p: tuple[int, int] = Depends(pagination)):
    skip, limit = p
    return {"skip": skip, "limit": limit}


@app.get("/things")
async def list_things(p: tuple[int, int] = Depends(pagination)):
    skip, limit = p
    return {"skip": skip, "limit": limit}
