from fastapi import Cookie, FastAPI

app = FastAPI()


@app.get("/")
async def get_cookie(hello: str | None = Cookie(None)):
    return {"hello": hello}
