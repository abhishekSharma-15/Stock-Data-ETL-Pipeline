from minio import Minio
import json
import asyncio
import io
from src.utils.interface import ObjectRepo
from src.utils.config import MINIO_BUCKET

class ObjectRepository(ObjectRepo):

    def __init__(self, client: Minio):
        self.client = client    
        self.bucket_name = MINIO_BUCKET

    async def upload_object(
        self,
        object_name: str,
        payload: dict | list
    ) -> None:
        
        data = json.dumps(payload, indent=2).encode("utf-8")
        await asyncio.to_thread(
            self.client.put_object,
            bucket_name=self.bucket_name,
            object_name=object_name,
            data=io.BytesIO(data),
            length=len(data),
            content_type="application/json"
        )