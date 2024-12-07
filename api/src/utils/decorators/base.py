import asyncio
from functools import wraps
from time import time

from src.utils.cache_manager import cache_manager


def process_time():
    """Print process execution time for a given function"""

    def decorator(func):
        if asyncio.iscoroutinefunction(func):

            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                start_time = time()
                response = await func(*args, **kwargs)

                time_diff = f"{(time() - start_time):.2f}s"
                print(f"Execution time for {func.__name__}: {time_diff}")

                return response

            return async_wrapper

        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time()
            response = func(*args, **kwargs)

            time_diff = f"{(time() - start_time):.2f}s"
            print(f"Execution time for {func.__name__}: {time_diff}")

            return response

        return wrapper

    return decorator


def use_cache_manager(cache_key: str, expiry=86400):
    """decorator to use cache manager"""

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache = await cache_manager(cache_key)
            if cache:
                value = cache.get("cached_value")
                if value:
                    return value

            result = await func(*args, **kwargs)

            if result and cache:
                redis = cache.get("redis")
                await redis.set(cache_key, result, ex=expiry)

            return result

        return wrapper

    return decorator
