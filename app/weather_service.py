import datetime
from http.client import HTTPException

from app.aiohttp_maneger import AiohttpManager
from app.dynamodb_manager import DynamoDBClient
from app.minio_manager import MinioManager
from app.redis_manager import RedisClient
from app.settings import WEATHER_BASE_API_URL


class WeatherService:
    def __init__(
            self, db_client: DynamoDBClient,
            aiohttp_manager: AiohttpManager,
            redis_manager: RedisClient,
            minio_manager: MinioManager
    ):
        self.db_client = db_client
        self.aiohttp_manager = aiohttp_manager
        self.redis_manager = redis_manager
        self.minio_manager = minio_manager

    async def get_weather(self, city: str) -> dict:

        cached_weather_data = await self.redis_manager.get_cache(city)
        if not cached_weather_data:
            api_url = f"{WEATHER_BASE_API_URL}{city}?format=j1"
            weather_data = await self.aiohttp_manager.get(api_url)

            if not weather_data:
                print(f'error while fetching weather data')
                raise HTTPException('error while fetching weather data')

            temp = weather_data['current_condition'][0]['temp_C']
            current_temp = {"city": city, "temp": temp}
            await self.redis_manager.set_cache(city, temp)
        else:
            current_temp = {"city": city, "temp": cached_weather_data}

        s3_url = await self.minio_manager.save_weather_response(city, current_temp)

        log_data = {
            "Location": city,
            "Timestamp": datetime.datetime.utcnow().isoformat(),
            "S3Url": s3_url
        }
        await self.db_client.log_event(log_data)

        return current_temp
