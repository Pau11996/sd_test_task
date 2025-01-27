import aiohttp
from typing import Any, Dict, Optional


class AiohttpManager:
    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout

    async def _request(self, method: str, endpoint: str, **kwargs) -> Any:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
            async with session.request(method, endpoint, **kwargs) as response:
                response.raise_for_status()
                try:
                    return await response.json()
                except aiohttp.ContentTypeError:
                    return None

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
