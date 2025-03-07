from typing import List, Optional
from uuid import UUID

from models.coach.coach import Coach
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import subqueryload


class CoachRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, coach: Coach) -> Coach:
        self.db.add(coach)
        await self.db.commit()
        await self.db.refresh(coach)
        return coach

    async def get(self, coach_id: UUID) -> Optional[Coach]:
        query = select(Coach).options(subqueryload(Coach.users)).where(Coach.id == coach_id)
        result = await self.db.execute(query)
        coach: Coach | None = result.scalar_one_or_none()
        return coach

    async def get_all(self) -> List[Coach]:
        query = select(Coach).options(subqueryload(Coach.users))
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def update(self, coach_id: UUID, coach_data: Coach) -> Optional[Coach]:
        db_coach = await self.get(coach_id)
        if db_coach:
            for key, value in coach_data.dict(exclude_unset=True).items():
                setattr(db_coach, key, value)
            self.db.add(db_coach)
            await self.db.commit()
            await self.db.refresh(db_coach)
            return db_coach
        return None

    async def delete(self, coach_id: UUID) -> bool:
        db_coach = await self.get(coach_id)
        if db_coach:
            await self.db.delete(db_coach)
            await self.db.commit()
            return True
        return False
