from datetime import date
from typing import Any, Callable, Coroutine, List

from constants.prefixes import Prefixes
from constants.status_enum import CompetitionStatus
from dependencies import async_get_db, get_redis_client
from fastapi import Depends, HTTPException
from models import TrainingCamp, TrainingCampDay
from pydantic import UUID4
from repositories.training_camp.training_camp_repository import TrainingCampRepository
from repositories.training_camp_days.training_camp_days_repository import TrainingCampDaysRepository
from schemas.auth.redis_session_data import RedisSessionData
from schemas.training_camp.training_camp_create_request import TrainingCampCreateRequest
from schemas.training_camp.training_camp_schema import TrainingCampSchema
from schemas.training_camp.training_camp_update_request import TrainingCampUpdateRequest
from schemas.training_camp.training_camp_view import TrainingCampViewSchema
from schemas.training_camp_day.training_camp_day_schema import TrainingCampDaySchema
from schemas.training_camp_day.training_camp_update_request import TrainingCampDayUpdateRequest
from services.redis import RedisClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status


class TrainingCampService:

    def __init__(
        self,
        db: AsyncSession = Depends(async_get_db),
        redis_client: RedisClient = Depends(get_redis_client),
    ):
        self.camp_repository: TrainingCampRepository = TrainingCampRepository(db)
        self.camp_days_repository: TrainingCampDaysRepository = TrainingCampDaysRepository(db)
        self.redis_client: RedisClient = redis_client

    async def create(self, data: TrainingCampCreateRequest, sid: str):
        dict = self.redis_client.get(f"{Prefixes.redis_session_prefix.value}:{sid}")
        user = RedisSessionData(**dict)
        await self.camp_repository.create(TrainingCamp(**data.model_dump(), user_id=user.id))

    async def get_all(self, sid: str, current_date: date, status: CompetitionStatus):
        dict = self.redis_client.get(f"{Prefixes.redis_session_prefix.value}:{sid}")
        data = RedisSessionData(**dict)
        callback = self.get_all_by_status(status)
        camps = await callback(data.id, current_date)
        camps_schemas = [TrainingCampSchema.model_validate(camp) for camp in camps]
        return camps_schemas

    async def get_all_days(self, id: UUID4):
        days = await self.camp_repository.get_all_days(id)
        days_schemas = [TrainingCampViewSchema.model_validate(day) for day in days]
        return days_schemas

    async def get_info(self, id: UUID4):
        camp = await self.camp_repository.get(id)
        if camp is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Camp not found")
        return TrainingCampSchema.model_validate(camp)

    def get_all_by_status(
        self, status: CompetitionStatus
    ) -> Callable[[str, date], Coroutine[Any, Any, List[TrainingCamp]]]:
        match status:
            case CompetitionStatus.past:
                return self.camp_repository.get_all_previous_camps
            case CompetitionStatus.current:
                return self.camp_repository.get_all_current_camps
            case CompetitionStatus.next:
                return self.camp_repository.get_all_future_camps

    async def update(self, id: UUID4, data: TrainingCampUpdateRequest):
        new_camp = await self.camp_repository.update(id, data)
        if new_camp is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Camp not found")
        return TrainingCampSchema.model_validate(new_camp)

    async def delete(self, camp_id: UUID4):
        res = await self.camp_repository.delete(camp_id)
        if not res:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Camp not found")

    async def get_camp_day(self, camp_id: UUID4, day: date):
        day_model = await self.camp_days_repository.get_day(camp_id, day)
        camp = await self.camp_repository.get(camp_id)
        res = TrainingCampDaySchema(
            id=day_model.id if day_model else None,
            camp_start_date=camp.start_date,
            camp_end_date=camp.end_date,
            camp_location=camp.location,
            date=day,
            goals=day_model.goals if day_model else "",
            notes=day_model.notes if day_model else "",
        )
        return res

    async def update_camp_day(self, id: UUID4, body: TrainingCampDayUpdateRequest):
        if body.id:
            day = await self.camp_days_repository.get_day(id, body.date)
            if not day:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Camp day not found"
                )
            new_day = await self.camp_days_repository.update(id, body)
        else:
            day_model = TrainingCampDay()
            day_model.training_camp_id = id
            day_model.notes = body.notes
            day_model.goals = body.goals
            day_model.date = body.date
            new_day = await self.camp_days_repository.create(day_model)
        return new_day
