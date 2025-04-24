from datetime import date
from typing import Callable, List

from constants.ant_params_category_enum import AnthropometricParamsMeasures
from constants.prefixes import Prefixes
from dependencies import async_get_db, get_redis_client
from fastapi import Depends, HTTPException
from models import AnthropometricParams
from pydantic import UUID4
from repositories.ant_params.anthropometric_params_repository import AnthropometricParamsRepository
from schemas.ant_params.ant_params_create_request import AnthropometricParamsCreateRequest
from schemas.ant_params.ant_params_schema import AnthropometricParamsSchema
from schemas.ant_params.ant_params_update_request import AnthropometricParamsUpdateRequest
from schemas.ant_params.ant_params_view import AnthropometricParamsView
from schemas.auth.redis_session_data import RedisSessionData
from schemas.general.graphic_data import GraphicPoint
from services.redis import RedisClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status


class AnthropometricParamsService:

    def __init__(
        self,
        db: AsyncSession = Depends(async_get_db),
        redis_client: RedisClient = Depends(get_redis_client),
    ):
        self.ant_params_repository: AnthropometricParamsRepository = AnthropometricParamsRepository(
            db
        )
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
        results_schema = [AnthropometricParamsView.model_validate(result) for result in results]
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

    async def get_graphic_data(
        self, start_date: date, end_date: date, category: AnthropometricParamsMeasures, sid: UUID4
    ):
        dict = self.redis_client.get(f"{Prefixes.redis_session_prefix.value}:{sid}")
        user = RedisSessionData(**dict)
        res = await self.ant_params_repository.get_graphic_data(start_date, end_date, user.id)
        selector = self.get_selector(category)
        filtered_data = selector(res)
        return filtered_data

    def get_selector(
        self, category: AnthropometricParamsMeasures
    ) -> Callable[[List[AnthropometricParams]], List[GraphicPoint]]:
        match category:
            case AnthropometricParamsMeasures.weight:
                return lambda dataList: [
                    GraphicPoint(
                        key=param.date,
                        value=param.weight,
                    )
                    for param in dataList
                ]
            case AnthropometricParamsMeasures.height:
                return lambda dataList: [
                    GraphicPoint(
                        key=param.date,
                        value=param.height,
                    )
                    for param in dataList
                ]
            case AnthropometricParamsMeasures.chestCircumference:
                return lambda dataList: [
                    GraphicPoint(
                        key=param.date,
                        value=param.chest_circumference,
                    )
                    for param in dataList
                ]
