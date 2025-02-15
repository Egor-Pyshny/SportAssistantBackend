from functools import wraps
from typing import Callable

from constants.exceptions import Exceptions
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status


def async_transaction(func: Callable):
    @wraps(func)
    async def wrapper(db: AsyncSession, *args, **kwargs):
        try:
            result = await func(db, *args, **kwargs)
            return result
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=Exceptions.transaction_failed.value,
            )

    return wrapper
