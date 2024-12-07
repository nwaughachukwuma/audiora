import asyncio
from dataclasses import dataclass
from functools import wraps
from time import sleep
from typing import Any


@dataclass
class RetryConfig:
    retries: int = 3
    delay: float = 1.0
    backoff: float | None = None


def retry(retry_config: RetryConfig | None, default_return: Any = None) -> Any:
    """
    Retry logic for async functions with exponential backoff.
    """
    config = retry_config or RetryConfig()

    def decorator(func):
        if asyncio.iscoroutinefunction(func):

            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                async def _async_retry():
                    delay = config.delay
                    for attempt in range(config.retries):
                        try:
                            return await func(*args, **kwargs)
                        except Exception as e:
                            print(f"Retry attempt {attempt + 1}/{config.retries} failed: {e}")
                            await asyncio.sleep(delay)
                            if config.backoff:
                                delay *= config.backoff

                    return default_return

                return await _async_retry()

            return async_wrapper

        @wraps(func)
        def wrapper(*args, **kwargs):
            def _sync_retry():
                delay = config.delay
                for attempt in range(config.retries):
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        print(f"Retry attempt {attempt + 1}/{config.retries} failed: {e}")
                        sleep(delay)
                        if config.backoff:
                            delay *= config.backoff

                return default_return

            return _sync_retry()

        return wrapper

    return decorator
