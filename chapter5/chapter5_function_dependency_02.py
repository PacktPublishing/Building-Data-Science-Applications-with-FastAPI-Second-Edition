from fastapi import Depends, FastAPI, Query

app = FastAPI()


async def pagination(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=0),
) -> tuple[int, int]:
    capped_limit = min(100, limit)
    return (skip, capped_limit)


@app.get("/items")
async def list_items(p: tuple[int, int] = Depends(pagination)):
    skip, limit = p
    return {"skip": skip, "limit": limit}


@app.get("/things")
async def list_things(p: tuple[int, int] = Depends(pagination)):
    skip, limit = p
    return {"skip": skip, "limit": limit}
