from typing import Optional

from redis.asyncio import Redis as AsyncRedis

from src.env_var import REDIS_HOST, REDIS_PASSWORD


class RedisClient:
    _instance: Optional[AsyncRedis] = None

    def __new__(cls) -> AsyncRedis:
        """
        Singleton pattern for redis client
        """
        if not cls._instance:
            cls._instance = cls._create_instance()
        return cls._instance

    @classmethod
    def _create_instance(cls) -> AsyncRedis:
        """
        Initialize an asynchronous Redis client
        """
        return AsyncRedis(
            password=REDIS_PASSWORD,
            port=6379,
            host=REDIS_HOST,
            ssl=True,
        )


def get_redis() -> AsyncRedis:
    """Return asynchronous Redis object"""
    return RedisClient()
