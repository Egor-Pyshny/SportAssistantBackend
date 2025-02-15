from pydantic import EmailStr
from starlette import status

from constants.prefixes import Prefixes
from dependencies import async_get_db, get_redis_client
from fastapi import Depends, HTTPException
from repositories.user.user_repository import UserRepository
from schemas.auth.redis_session_data import RedisSessionData
from schemas.user.user_response_schema import UserResponseSchema
from services.redis import RedisClient
from sqlalchemy.ext.asyncio import AsyncSession


class UserService:

    def __init__(
        self,
        db: AsyncSession = Depends(async_get_db),
        redis_client: RedisClient = Depends(get_redis_client),
    ):
        self.user_repository: UserRepository = UserRepository(db)
        self.redis_client: RedisClient = redis_client

    async def get_me(self, sid: str):
        dict = self.redis_client.get(f"{Prefixes.redis_session_prefix.value}:{sid}")
        data = RedisSessionData(**dict)
        user_data = await self.user_repository.get_user_by_email(data.email)
        if not user_data:
            raise HTTPException(status_code=403)
        return UserResponseSchema.model_validate(user_data)

    async def check_email(self, email: str | EmailStr):
        if await self.user_repository.is_unique_email(email=email):
            raise HTTPException(
                detail={"message": "Email already taken"},
                status_code=status.HTTP_409_CONFLICT,
            )
