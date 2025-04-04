from datetime import date

from constants.prefixes import Prefixes
from dependencies import async_get_db, get_redis_client
from fastapi import Depends, HTTPException
from models import OFPResults
from pydantic import UUID4
from repositories.ofp_results.ofp_results_repository import OFPResultsRepository
from schemas.auth.redis_session_data import RedisSessionData
from schemas.general.category_schema import CategorySchema
from schemas.general.graphic_data import GraphicPoint
from schemas.ofp_results.ofp_result_create_request import OFPResultCreateRequest
from schemas.ofp_results.ofp_result_schema import OFPResultSchema
from schemas.ofp_results.ofp_result_update_request import OFPResultUpdateRequest
from schemas.ofp_results.ofp_results_view import OFPResultViewSchema
from services.redis import RedisClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status


class OFPResultsService:

    def __init__(
        self,
        db: AsyncSession = Depends(async_get_db),
        redis_client: RedisClient = Depends(get_redis_client),
    ):
        self.ofp_results_repository: OFPResultsRepository = OFPResultsRepository(db)
        self.redis_client: RedisClient = redis_client

    async def get_categories(self):
        categories = await self.ofp_results_repository.get_categories()
        categories_schema = [CategorySchema.model_validate(category) for category in categories]
        return categories_schema

    async def create(self, body: OFPResultCreateRequest, sid: str):
        dict = self.redis_client.get(f"{Prefixes.redis_session_prefix.value}:{sid}")
        user = RedisSessionData(**dict)
        await self.ofp_results_repository.create(OFPResults(**body.model_dump(), user_id=user.id))

    async def get_all(self, sid: str):
        dict = self.redis_client.get(f"{Prefixes.redis_session_prefix.value}:{sid}")
        user = RedisSessionData(**dict)
        results = await self.ofp_results_repository.get_all(user.id)
        results_schema = [OFPResultViewSchema.model_validate(result) for result in results]
        return results_schema

    async def delete(self, ofp_id: UUID4):
        res = await self.ofp_results_repository.delete(ofp_id)
        if not res:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="OFPResult not found")

    async def update(self, body: OFPResultUpdateRequest, ofp_id: UUID4):
        new_result = await self.ofp_results_repository.update(body, ofp_id)
        if new_result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="OFPResult not found")
        return OFPResultSchema.model_validate(new_result)

    async def get(self, ofp_id: UUID4):
        res = await self.ofp_results_repository.get(ofp_id)
        if res is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="OFPResult not found")
        schema = OFPResultSchema.model_validate(res)
        return schema

    async def get_graphic_data(
        self, start_date: date, end_date: date, category_id: UUID4, sid: UUID4
    ):
        dict = self.redis_client.get(f"{Prefixes.redis_session_prefix.value}:{sid}")
        user = RedisSessionData(**dict)
        res = await self.ofp_results_repository.get_graphic_data(
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
