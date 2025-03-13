from datetime import date

from pydantic import UUID4
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from models import TrainingCampDay
from schemas.training_camp_day.training_camp_update_request import TrainingCampDayUpdateRequest


class TrainingCampDaysRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, new_camp_day: TrainingCampDay) -> TrainingCampDay:
        self.db.add(new_camp_day)
        await self.db.commit()
        await self.db.refresh(new_camp_day)
        return new_camp_day

    async def get_day(self, camp_id: UUID4, day: date):
        query = select(TrainingCampDay).where(
            and_(TrainingCampDay.training_camp_id == camp_id, TrainingCampDay.date == day)
        )
        result = await self.db.execute(query)
        camp: TrainingCampDay | None = result.scalar_one_or_none()
        return camp

    async def update(self, camp_id: UUID4, data: TrainingCampDayUpdateRequest):
        query = select(TrainingCampDay).where(
            and_(TrainingCampDay.training_camp_id == camp_id, TrainingCampDay.date == data.date)
        )
        result = await self.db.execute(query)
        camp_day: TrainingCampDay | None = result.scalar_one_or_none()
        if camp_day:
            camp_day.notes = data.notes
            camp_day.goals = data.goals
            self.db.add(camp_day)
            await self.db.commit()
            await self.db.refresh(camp_day)
            return camp_day
        return None
