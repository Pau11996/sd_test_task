import aiofiles
from minio import Minio
from minio.error import S3Error
import json
import datetime


class MinioManager:
    def __init__(self, endpoint, access_key, secret_key, bucket_name):
        self.client = Minio(
            endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=endpoint.startswith("https")
        )
        self.bucket_name = bucket_name

        if not self.client.bucket_exists(bucket_name):
            self.client.make_bucket(bucket_name)

    async def save_weather_response(self, city, json_weather_data):
        filename = f"{city}_{datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')}.json"
        filepath = f"/tmp/{filename}"
        async with aiofiles.open(filepath, mode="w") as file:
            await file.write(json.dumps(json_weather_data))

        try:
            self.client.fput_object(self.bucket_name, filename, filepath)
            print(f"File {filename} successfully uploaded to bucket {self.bucket_name}.")

            url = self.client.presigned_get_object(self.bucket_name, filename)
            return url
        except S3Error as e:
            print(f"Error uploading file {filename} to bucket {self.bucket_name}: {e}")
