import os
from collections.abc import AsyncGenerator
from typing import Annotated

from constants.prefixes import Prefixes
from database import AsyncSessionFactory
from fastapi import Cookie, HTTPException, status
from services.mail import MailSender, SMTPClient
from services.redis import RedisClient
from sqlalchemy.ext.asyncio import AsyncSession


def get_redis_client() -> RedisClient:
    return RedisClient(
        host=os.getenv("REDIS_HOST", "localhost"), port=int(os.getenv("REDIS_PORT", 6379))
    )


def authorized_only(sid: Annotated[str | None, Cookie()] = None):
    sid = "e0ef4945a37e6ee7721e49a845297811ba89eca4455882aefca7a8b87700bc66"
    redis_client = get_redis_client()
    data = redis_client.get(f"{Prefixes.redis_session_prefix.value}:{sid}") if sid else None
    if not sid or not data:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    # new_sid = generate_sid()
    # redis_client.set(f"{Prefixes.redis_session_prefix.value}:{new_sid}", data)
    # redis_client.delete(f"{Prefixes.redis_session_prefix.value}:{sid}")
    # return new_sid
    return sid


def get_mail_sender_client() -> MailSender:
    return SMTPClient()


async def async_get_db() -> AsyncGenerator[AsyncSession, Exception]:
    async with AsyncSessionFactory() as session:
        try:
            yield session
        except Exception as e:
            print(f"An error occurred: {e}")
            raise e
