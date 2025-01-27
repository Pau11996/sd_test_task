from fastapi import Request
from app.weather_service import WeatherService

def get_weather_service(request: Request) -> WeatherService:
    return request.app.state.weather_service