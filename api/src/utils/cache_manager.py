from typing import Any

from redis.asyncio import Redis
from typing_extensions import TypedDict

from src.services.redis_client import get_redis

ONE_DAY = 86400
ONE_MONTH = ONE_DAY * 30


class CacheManagerResponse(TypedDict):
    """Cache manager response object"""

    cached_value: str | None
    redis: Redis


async def cache_manager(cache_key: str) -> CacheManagerResponse | None:
    try:
        redis = get_redis()
        cached_value = await redis.get(cache_key)
        resolved_value = process_cached_value(cached_value) if cached_value else None
        return CacheManagerResponse(cached_value=resolved_value, redis=redis)
    except Exception as err:
        print("Failed to get redis client %s", err)
        return None


def process_cached_value(input_string: Any):
    if isinstance(input_string, bytes):
        return input_string.decode("utf-8")
    else:
        return str(input_string)
