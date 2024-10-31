import asyncio
from functools import wraps
from time import time


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
