from datetime import date
from typing import Any, Callable, Coroutine, List

from constants.prefixes import Prefixes
from constants.status_enum import CompetitionStatus
from dependencies import async_get_db, get_redis_client
from fastapi import HTTPException
from fastapi.params import Depends
from models import Competition, CompetitionDay, CompetitionResult
from pydantic import UUID4
from repositories.competition.competition_repository import CompetitionRepository
from repositories.competition_days.competition_days_repository import CompetitionDaysRepository
from repositories.competition_result.competition_result_repository import (
    CompetitionResultRepository,
)
from schemas.auth.redis_session_data import RedisSessionData
from schemas.competition.competition_create_request import CompetitionCreateRequest
from schemas.competition.competition_schema import CompetitionSchema
from schemas.competition.competition_update_request import CompetitionUpdateRequest
from schemas.competition.competition_view import CompetitionViewSchema
from schemas.competition_day.competition_day_schema import CompetitionDaySchema
from schemas.competition_day.competition_day_update_request import CompetitionDayUpdateRequest
from schemas.competition_result.competition_result_schema import CompetitionResultSchema
from schemas.competition_result.competition_result_update_request import (
    CompetitionResultUpdateRequest,
)
from services.redis import RedisClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status


class CompetitionService:

    def __init__(
        self,
        db: AsyncSession = Depends(async_get_db),
        redis_client: RedisClient = Depends(get_redis_client),
    ):
        self.competition_repository: CompetitionRepository = CompetitionRepository(db)
        self.competition_days_repository: CompetitionDaysRepository = CompetitionDaysRepository(db)
        self.competition_result_repository: CompetitionResultRepository = (
            CompetitionResultRepository(db)
        )
        self.redis_client: RedisClient = redis_client

    async def create(self, data: CompetitionCreateRequest, sid: str):
        dict = self.redis_client.get(f"{Prefixes.redis_session_prefix.value}:{sid}")
        user = RedisSessionData(**dict)
        competition = await self.competition_repository.create(
            Competition(**data.model_dump(), user_id=user.id)
        )
        result = CompetitionResult()
        result.competition_id = competition.id
        result.competition = competition
        await self.competition_result_repository.create(result)

    async def get_all(self, sid: str, current_date: date, status: CompetitionStatus):
        dict = self.redis_client.get(f"{Prefixes.redis_session_prefix.value}:{sid}")
        data = RedisSessionData(**dict)
        callback = self.get_all_by_status(status)
        competitions = await callback(data.id, current_date)
        competitions_schemas = [
            CompetitionViewSchema.model_validate(competition) for competition in competitions
        ]
        return competitions_schemas

    async def get_all_days(self, id: UUID4):
        days = await self.competition_repository.get_all_days(id)
        days_schemas = [CompetitionDaySchema.model_validate(day) for day in days]
        return days_schemas

    async def get_info(self, id: UUID4):
        competition = await self.competition_repository.get(id)
        if competition is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Competition not found"
            )
        return CompetitionSchema.model_validate(competition)

    def get_all_by_status(
        self, status: CompetitionStatus
    ) -> Callable[[str, date], Coroutine[Any, Any, List[Competition]]]:
        match status:
            case CompetitionStatus.past:
                return self.competition_repository.get_all_previous_competitions
            case CompetitionStatus.current:
                return self.competition_repository.get_all_current_competitions
            case CompetitionStatus.next:
                return self.competition_repository.get_all_future_competitions

    async def update(self, id: UUID4, data: CompetitionUpdateRequest):
        new_competition = await self.competition_repository.update(id, data)
        if new_competition is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Competition not found"
            )
        return CompetitionSchema.model_validate(new_competition)

    async def delete(self, competition_id: UUID4):
        res = await self.competition_repository.delete(competition_id)
        if not res:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Competition not found"
            )

    async def get_competition_day(self, competition_id: UUID4, day: date):
        day_model = await self.competition_days_repository.get_day(competition_id, day)
        competition = await self.competition_repository.get(competition_id)
        res = CompetitionDaySchema(
            id=day_model.id if day_model else None,
            date=day,
            competition_start_date=competition.start_date,
            competition_end_date=competition.end_date,
            competition_location=competition.location,
            competition_name=competition.name,
            results=day_model.results if day_model else "",
            notes=day_model.notes if day_model else "",
        )
        return res

    async def update_competition_day(self, id: UUID4, body: CompetitionDayUpdateRequest):
        if body.id:
            day = await self.competition_days_repository.get_day(id, body.date)
            if not day:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Competition day not found"
                )
            new_day = await self.competition_days_repository.update(id, body)
        else:
            day_model = CompetitionDay()
            day_model.competition_id = id
            day_model.notes = body.notes
            day_model.results = body.result
            day_model.date = body.date
            new_day = await self.competition_days_repository.create(day_model)
        return new_day

    async def get_competition_result(self, competition_id: UUID4):
        competition = await self.competition_repository.get(competition_id)
        if not competition:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Competition not found"
            )
        result = await self.competition_result_repository.get(competition_id)
        res = CompetitionResultSchema(
            id=result.id if result else None,
            competition_start_date=competition.start_date,
            competition_end_date=competition.end_date,
            competition_location=competition.location,
            competition_name=competition.name,
            results=result.results if result else "",
            notes=result.notes if result else "",
        )
        return res

    async def update_competition_result(
        self, competition_id: UUID4, body: CompetitionResultUpdateRequest
    ):
        result = await self.competition_result_repository.update(competition_id, body)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Competition not found"
            )
        return CompetitionResultSchema.model_validate(result)
