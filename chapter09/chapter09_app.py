import contextlib

from fastapi import FastAPI


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    print("Startup")
    yield
    print("Shutdown")


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def hello_world():
    return {"hello": "world"}
