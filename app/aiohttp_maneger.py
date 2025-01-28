import asyncio

import aiohttp
from typing import Any, Dict, Optional


class AiohttpManager:
    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout

    async def _request(self, method: str, endpoint: str, **kwargs) -> Any:
        max_retries = 3
        retry_delay = 1

        for attempt in range(max_retries):
            try:

                async with aiohttp.ClientSession(
                    timeout=aiohttp.ClientTimeout(total=self.timeout)
                ) as session:
                    async with session.request(method, endpoint, **kwargs) as response:
                        response.raise_for_status()
                        return await response.json()
            except (aiohttp.ClientResponseError, asyncio.TimeoutError):
                if attempt == max_retries - 1:
                    raise
                await asyncio.sleep(retry_delay)

    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None,
                  headers: Optional[Dict[str, str]] = None) -> Any:
        return await self._request("GET", endpoint, params=params, headers=headers)

    async def post(self, endpoint: str, data: Optional[Any] = None, json: Optional[Dict[str, Any]] = None,
                   headers: Optional[Dict[str, str]] = None) -> Any:
        return await self._request("POST", endpoint, data=data, json=json, headers=headers)

    async def put(self, endpoint: str, data: Optional[Any] = None, json: Optional[Dict[str, Any]] = None,
                  headers: Optional[Dict[str, str]] = None) -> Any:
        return await self._request("PUT", endpoint, data=data, json=json, headers=headers)

    async def delete(self, endpoint: str, headers: Optional[Dict[str, str]] = None) -> Any:
        return await self._request("DELETE", endpoint, headers=headers)
