from datetime import date, timedelta
from typing import Any, Callable, Coroutine, List

from constants.prefixes import Prefixes
from constants.status_enum import CompetitionStatus
from dependencies import async_get_db, get_redis_client
from fastapi import HTTPException
from fastapi.params import Depends
from models import Competition, CompetitionDay
from pydantic import UUID4
from repositories.competition.competition_repository import CompetitionRepository
from repositories.competition_days.competition_days_repository import CompetitionDaysRepository
from schemas.auth.redis_session_data import RedisSessionData
from schemas.competition.competition_create_request import CompetitionCreateRequest
from schemas.competition.competition_schema import CompetitionSchema
from schemas.competition.competition_update_request import CompetitionUpdateRequest
from schemas.competition_day.competition_day_schema import CompetitionDaySchema
from schemas.competition_day.competition_day_update_request import CompetitionDayUpdateRequest
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
        self.redis_client: RedisClient = redis_client

    async def create(self, data: CompetitionCreateRequest, sid: str):
        dict = self.redis_client.get(f"{Prefixes.redis_session_prefix.value}:{sid}")
        user = RedisSessionData(**dict)
        competition = await self.competition_repository.create(
            Competition(**data.model_dump(), user_id=user.id)
        )
        dates = [
            data.start_date + timedelta(days=i)
            for i in range((data.end_date - data.start_date).days + 1)
        ]

    async def get_all(self, sid: str, current_date: date, status: CompetitionStatus):
        dict = self.redis_client.get(f"{Prefixes.redis_session_prefix.value}:{sid}")
        data = RedisSessionData(**dict)
        callback = self.get_all_by_status(status)
        competitions = await callback(data.id, current_date)
        competitions_schemas = [
            CompetitionSchema.model_validate(competition) for competition in competitions
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
        competition = await self.competition_repository.get(competition_id)
        if not competition:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Competition not found"
            )
        competition_schema = CompetitionSchema.model_validate(competition)
        day_model = await self.competition_days_repository.get_day(competition_id, day)
        res = CompetitionDaySchema(
            id=day_model.id if day_model else None,
            date=day,
            results=day_model.results if day_model else "",
            notes=day_model.notes if day_model else "",
            competition_name=competition_schema.name,
            competition_location=competition_schema.location,
            competition_end_date=competition_schema.end_date,
            competition_start_date=competition_schema.start_date,
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
