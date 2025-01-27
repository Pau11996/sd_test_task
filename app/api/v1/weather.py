import traceback
from http.client import HTTPException

from aiohttp import ClientResponseError
from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from app.dependencies import get_weather_service
from app.weather_service import WeatherService

router = APIRouter(prefix='/weather', tags=['weather'])

@router.get("/{city}")
async def get_weather(location: str, weather_service: WeatherService = Depends(get_weather_service)):
    try:
        weather = await weather_service.get_weather(location)
        return JSONResponse(status_code=200, content=weather)
    except HTTPException as e:
        print(f'get_weather: HTTPException occured {str(e)}')
        return JSONResponse(status_code=400, content=str(e))
    except ClientResponseError as e:
        print(f'get_weather: ClientResponseError occured {str(e)}')
        return JSONResponse(status_code=404, content=str(e.message))
