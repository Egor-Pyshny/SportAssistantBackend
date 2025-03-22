from datetime import date

from constants.prefixes import Prefixes
from dependencies import async_get_db, get_redis_client
from fastapi import Depends, HTTPException
from models import SFPResults
from pydantic import UUID4
from repositories.sfp_results.sfp_results_repository import SFPResultsRepository
from schemas.auth.redis_session_data import RedisSessionData
from schemas.general.category_schema import CategorySchema
from schemas.general.graphic_data import GraphicPoint
from schemas.sfp_results.sfp_result_create_request import SFPResultCreateRequest
from schemas.sfp_results.sfp_result_schema import SFPResultSchema
from schemas.sfp_results.sfp_result_update_request import SFPResultUpdateRequest
from schemas.sfp_results.sfp_results_view import SFPResultViewSchema
from services.redis import RedisClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status


class SFPResultsService:

    def __init__(
        self,
        db: AsyncSession = Depends(async_get_db),
        redis_client: RedisClient = Depends(get_redis_client),
    ):
        self.sfp_results_repository: SFPResultsRepository = SFPResultsRepository(db)
        self.redis_client: RedisClient = redis_client

    async def get_categories(self):
        categories = await self.sfp_results_repository.get_categories()
        categories_schema = [CategorySchema.model_validate(category) for category in categories]
        return categories_schema

    async def create(self, body: SFPResultCreateRequest, sid: str):
        dict = self.redis_client.get(f"{Prefixes.redis_session_prefix.value}:{sid}")
        user = RedisSessionData(**dict)
        await self.sfp_results_repository.create(SFPResults(**body.model_dump(), user_id=user.id))

    async def get_all(self, sid: str):
        dict = self.redis_client.get(f"{Prefixes.redis_session_prefix.value}:{sid}")
        user = RedisSessionData(**dict)
        results = await self.sfp_results_repository.get_all(user.id)
        results_schema = [SFPResultViewSchema.model_validate(result) for result in results]
        return results_schema

    async def delete(self, sfp_id: UUID4):
        res = await self.sfp_results_repository.delete(sfp_id)
        if not res:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="SFPResult not found")

    async def update(self, body: SFPResultUpdateRequest, sfp_id: UUID4):
        new_result = await self.sfp_results_repository.update(body, sfp_id)
        if new_result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="SFPResult not found")
        return SFPResultSchema.model_validate(new_result)

    async def get(self, sfp_id: UUID4):
        res = await self.sfp_results_repository.get(sfp_id)
        if res is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="SFPResult not found")
        schema = SFPResultSchema.model_validate(res)
        return schema

    async def get_graphic_data(
        self, start_date: date, end_date: date, category_id: UUID4, sid: UUID4
    ):
        dict = self.redis_client.get(f"{Prefixes.redis_session_prefix.value}:{sid}")
        user = RedisSessionData(**dict)
        res = await self.sfp_results_repository.get_graphic_data(
            start_date, end_date, category_id, user.id
        )
        graphic_points = [
            GraphicPoint(
                value=result.result,
                key=result.date,
            )
            for result in res
        ]
        return graphic_points
