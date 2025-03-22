from datetime import date
from typing import List

from models import TrainingCamp, TrainingCampDay
from pydantic import UUID4
from schemas.training_camp.training_camp_update_request import TrainingCampUpdateRequest
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import subqueryload


class TrainingCampRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, new_camp: TrainingCamp) -> TrainingCamp:
        self.db.add(new_camp)
        await self.db.commit()
        await self.db.refresh(new_camp)
        return new_camp

    async def get_all_previous_camps(self, user_id: str, current_date: date) -> List[TrainingCamp]:
        query = select(TrainingCamp).where(
            and_(TrainingCamp.user_id == user_id, TrainingCamp.end_date < current_date)
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_all_current_camps(self, user_id: str, current_date: date) -> List[TrainingCamp]:
        query = select(TrainingCamp).where(
            and_(
                TrainingCamp.user_id == user_id,
                TrainingCamp.start_date <= current_date,
                TrainingCamp.end_date >= current_date,
            )
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_all_future_camps(self, user_id: str, current_date: date) -> List[TrainingCamp]:
        query = select(TrainingCamp).where(
            and_(TrainingCamp.user_id == user_id, TrainingCamp.start_date > current_date)
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_all(self, user_id: str, current_date: date) -> List[TrainingCamp]:
        query = select(TrainingCamp)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_all_days(self, id: str) -> List[TrainingCampDay]:
        query = (
            select(TrainingCampDay)
            .options(subqueryload(TrainingCampDay.days))
            .where(TrainingCampDay.id == id)
        )
        result = await self.db.execute(query)
        camp: TrainingCamp | None = result.scalar_one_or_none()
        return camp.days if camp else []

    async def get(self, id):
        query = select(TrainingCamp).where(TrainingCamp.id == id)
        result = await self.db.execute(query)
        camp: TrainingCamp | None = result.scalar_one_or_none()
        return camp

    async def update(self, id: UUID4, data: TrainingCampUpdateRequest):
        query = select(TrainingCamp).where(TrainingCamp.id == id)
        result = await self.db.execute(query)
        camp: TrainingCamp | None = result.scalar_one_or_none()
        if camp:
            camp.goals = data.goals
            camp.start_date = data.start_date
            camp.end_date = data.end_date
            camp.location = data.location
            camp.notes = data.notes
            self.db.add(camp)
            await self.db.commit()
            await self.db.refresh(camp)
            return camp
        return None

    async def delete(self, id: UUID4):
        query = select(TrainingCamp).where(TrainingCamp.id == id)
        result = await self.db.execute(query)
        camp: TrainingCamp | None = result.scalar_one_or_none()
        if camp:
            await self.db.delete(camp)
            await self.db.commit()
            return True
        return False
