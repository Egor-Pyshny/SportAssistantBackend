from typing import Optional

import redis
from pydantic import EmailStr


class RedisClient:
    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0):
        self.redis = redis.Redis(host=host, port=port, db=db, decode_responses=True)

    def set(
        self,
        key: str | EmailStr,
        value: dict,
        expire: Optional[int] = None,
    ) -> None:
        self.redis.hset(key, mapping=value)
        self.redis.expire(key, expire)

    def get(self, key: str | EmailStr) -> dict | None:
        value = self.redis.hgetall(key)
        return value if value else None

    def delete(self, key: str | EmailStr) -> bool:
        return bool(self.redis.delete(key))

    def exists(self, key: str | EmailStr) -> bool:
        return self.redis.exists(key) > 0

    def expire(self, key: str, seconds: int) -> bool:
        return self.redis.expire(key, seconds)

    def keys(self, pattern: str = "*") -> list:
        return [key for key in self.redis.keys(pattern)]
