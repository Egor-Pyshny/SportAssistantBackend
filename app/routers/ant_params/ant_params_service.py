from fastapi import Depends, HTTPException
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from constants.prefixes import Prefixes
from dependencies import async_get_db, get_redis_client
from models import AnthropometricParams
from repositories.ant_params.anthropometric_params_repository import AnthropometricParamsRepository
from schemas.ant_params.ant_params_create_request import AnthropometricParamsCreateRequest
from schemas.ant_params.ant_params_schema import AnthropometricParamsSchema
from schemas.ant_params.ant_params_update_request import AnthropometricParamsUpdateRequest
from schemas.ant_params.ant_params_view import AnthropometricParamsView
from schemas.auth.redis_session_data import RedisSessionData
from services.redis import RedisClient


class AnthropometricParamsService:

    def __init__(
        self,
        db: AsyncSession = Depends(async_get_db),
        redis_client: RedisClient = Depends(get_redis_client),
    ):
        self.ant_params_repository: AnthropometricParamsRepository = AnthropometricParamsRepository(db)
        self.redis_client: RedisClient = redis_client

    async def create(self, body: AnthropometricParamsCreateRequest, sid: str):
        dict = self.redis_client.get(f"{Prefixes.redis_session_prefix.value}:{sid}")
        user = RedisSessionData(**dict)
        await self.ant_params_repository.create(
            AnthropometricParams(**body.model_dump(), user_id=user.id)
        )

    async def get_all(self, sid: str):
        dict = self.redis_client.get(f"{Prefixes.redis_session_prefix.value}:{sid}")
        user = RedisSessionData(**dict)
        results = await self.ant_params_repository.get_all(user.id)
        results_schema = [
            AnthropometricParamsView.model_validate(result) for result in results
        ]
        return results_schema

    async def delete(self, params_id: UUID4):
        res = await self.ant_params_repository.delete(params_id)
        if not res:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="AnthropometricParams not found"
            )

    async def update(self, body: AnthropometricParamsUpdateRequest, params_id: UUID4):
        new_result = await self.ant_params_repository.update(body, params_id)
        if new_result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="AnthropometricParams not found"
            )
        return AnthropometricParamsSchema.model_validate(new_result)

    async def get(self, params_id: UUID4):
        res = await self.ant_params_repository.get(params_id)
        if res is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="AnthropometricParams not found"
            )
        schema = AnthropometricParamsSchema.model_validate(res)
        return schema
