import contextlib

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from chapter14.complete import schemas
from chapter14.complete.database import create_all_tables, get_async_session
from chapter14.complete.models import GeneratedImage
from chapter14.complete.settings import settings
from chapter14.complete.storage import Storage
from chapter14.complete.worker import text_to_image_task


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    await create_all_tables()
    yield


app = FastAPI(lifespan=lifespan)


async def get_generated_image_or_404(
    id: int, session: AsyncSession = Depends(get_async_session)
) -> GeneratedImage:
    select_query = select(GeneratedImage).where(GeneratedImage.id == id)
    result = await session.execute(select_query)
    image = result.scalar_one_or_none()

    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return image


async def get_storage() -> Storage:
    return Storage()


@app.post(
    "/generated-images",
    response_model=schemas.GeneratedImageRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_generated_image(
    generated_image_create: schemas.GeneratedImageCreate,
    session: AsyncSession = Depends(get_async_session),
) -> GeneratedImage:
    image = GeneratedImage(**generated_image_create.dict())
    session.add(image)
    await session.commit()

    text_to_image_task.send(image.id)

    return image


@app.get("/generated-images/{id}", response_model=schemas.GeneratedImageRead)
async def get_generated_image(
    image: GeneratedImage = Depends(get_generated_image_or_404),
) -> GeneratedImage:
    return image


@app.get("/generated-images/{id}/url")
async def get_generated_image_url(
    image: GeneratedImage = Depends(get_generated_image_or_404),
    storage: Storage = Depends(get_storage),
) -> schemas.GeneratedImageURL:
    if image.file_name is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Image is not available yet. Please try again later.",
        )

    url = storage.get_presigned_url(image.file_name, settings.storage_bucket)
    return schemas.GeneratedImageURL(url=url)
