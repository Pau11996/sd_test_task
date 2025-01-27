import json

import aioredis


class RedisClient:
    def __init__(self, redis_url):
        self.redis = aioredis.from_url(redis_url, decode_responses=True)

    async def set_cache(self, key, value, ttl=300):
        await self.redis.set(key, json.dumps(value), ex=ttl)

    async def get_cache(self, key):
        cached_value = await self.redis.get(key)
        if cached_value:
            return json.loads(cached_value)
        return None

    async def clear_cache(self, key):
        await self.redis.delete(key)