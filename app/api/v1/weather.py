import asyncio
from http.client import HTTPException

from aiohttp import ClientResponseError
from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from app.dependencies import get_weather_service
from app.weather_service import WeatherService

router = APIRouter(prefix='', tags=['weather'])

@router.get('/weather')
async def get_weather(city: str, weather_service: WeatherService = Depends(get_weather_service)):
    try:
        weather = await weather_service.get_weather(city)
        return JSONResponse(status_code=200, content=weather)
    except HTTPException as e:
        print(f'get_weather: HTTPException occured {str(e)}')
        return JSONResponse(status_code=400, content=str(e))
    except asyncio.TimeoutError as e:
        print(f'get_weather: error when accessing weather api, {str(e)}')
        return JSONResponse(status_code=400, content=str(e))
    except ClientResponseError as e:
        print(f'get_weather: ClientResponseError occured {str(e)}')
        return JSONResponse(status_code=404, content=str(e.message))
    except Exception as e:
        print(f'get_weather: unexpected error, {str(e)}')
        return JSONResponse(status_code=400, content=str(e))

