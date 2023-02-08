from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()


@app.get("/cat")
async def get_cat():
    root_directory = Path(__file__).parent.parent
    picture_path = root_directory / "assets" / "cat.jpg"
    return FileResponse(picture_path)
