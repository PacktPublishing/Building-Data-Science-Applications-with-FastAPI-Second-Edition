import io
from datetime import timedelta

from minio import Minio
from PIL.Image import Image

from chapter14.complete.settings import settings


class Storage:
    def __init__(self) -> None:
        self.client = Minio(
            settings.storage_endpoint,
            access_key=settings.storage_access_key,
            secret_key=settings.storage_secret_key,
        )

    def ensure_bucket(self, bucket_name: str):
        bucket_exists = self.client.bucket_exists(bucket_name)
        if not bucket_exists:
            self.client.make_bucket(bucket_name)

    def upload_image(self, image: Image, object_name: str, bucket_name: str):
        self.ensure_bucket(bucket_name)

        image_data = io.BytesIO()
        image.save(image_data, format="PNG")
        image_data.seek(0)
        image_data_length = len(image_data.getvalue())

        self.client.put_object(
            bucket_name,
            object_name,
            image_data,
            length=image_data_length,
            content_type="image/png",
        )

    def get_presigned_url(
        self,
        object_name: str,
        bucket_name: str,
        *,
        expires: timedelta = timedelta(days=7)
    ) -> str:
        return self.client.presigned_get_object(
            bucket_name, object_name, expires=expires
        )
