
from fastapi import FastAPI
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from app import settings
from app.aiohttp_maneger import AiohttpManager
from app.api import router
from app.dynamodb_manager import DynamoDBClient
from app.minio_manager import MinioManager
from app.redis_manager import RedisClient
from app.weather_service import WeatherService

# All of these prints in application must be changed to logger

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:


    dynamo_client = DynamoDBClient(
        region_name="us-east-1", endpoint_url=settings.DYNAMO_DB_URL, table_name=settings.DYNAMO_DB_TABLE_NAME
    )
    aiohttp_manager = AiohttpManager('https://test.com/')
    redis_manager = RedisClient(redis_url=settings.REDIS_URL)
    minio_manager = MinioManager(
        endpoint="minio:9000",
        access_key=settings.MINIO_ACCESS_KEY,
        secret_key=settings.MINIO_SECRET,
        bucket_name="weather-data"
    )
    await dynamo_client.create_table_if_not_exists()

    weather_service = WeatherService(
        db_client=dynamo_client,
        aiohttp_manager=aiohttp_manager,
        minio_manager=minio_manager,
        redis_manager=redis_manager
    )
    app.state.weather_service = weather_service

    yield

app = FastAPI(title="Weather App", version="1.0.0", lifespan=lifespan)
app.include_router(router)

