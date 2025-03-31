from datetime import date
from typing import List

from models import Competition, CompetitionDay
from pydantic import UUID4
from schemas.competition.competition_update_request import CompetitionUpdateRequest
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import subqueryload


class CompetitionRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, new_competition: Competition) -> Competition:
        self.db.add(new_competition)
        await self.db.commit()
        await self.db.refresh(new_competition)
        return new_competition

    async def get_all_previous_competitions(
        self, user_id: str, current_date: date
    ) -> List[Competition]:
        query = select(Competition).where(
            and_(Competition.user_id == user_id, Competition.end_date < current_date)
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_all_current_competitions(
        self, user_id: str, current_date: date
    ) -> List[Competition]:
        query = select(Competition).where(
            and_(
                Competition.user_id == user_id,
                Competition.start_date <= current_date,
                Competition.end_date >= current_date,
            )
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_all_future_competitions(
        self, user_id: str, current_date: date
    ) -> List[Competition]:
        query = select(Competition).where(
            and_(Competition.user_id == user_id, Competition.start_date > current_date)
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_all(self, user_id: str, current_date: date) -> List[Competition]:
        query = select(Competition)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_all_days(self, id: str) -> List[CompetitionDay]:
        query = (
            select(Competition).options(subqueryload(Competition.days)).where(Competition.id == id)
        )
        result = await self.db.execute(query)
        competition: Competition | None = result.scalar_one_or_none()
        return competition.days if competition else []

    async def get(self, id):
        query = select(Competition).where(Competition.id == id)
        result = await self.db.execute(query)
        competition: Competition | None = result.scalar_one_or_none()
        return competition

    async def update(self, id: UUID4, data: CompetitionUpdateRequest):
        query = select(Competition).where(Competition.id == id)
        result = await self.db.execute(query)
        competition: Competition | None = result.scalar_one_or_none()
        if competition:
            competition.name = data.name
            competition.start_date = data.start_date
            competition.end_date = data.end_date
            competition.location = data.location
            competition.notes = data.notes
            self.db.add(competition)
            await self.db.commit()
            await self.db.refresh(competition)
            return competition
        return None

    async def delete(self, id: UUID4):
        query = select(Competition).where(Competition.id == id)
        result = await self.db.execute(query)
        competition: Competition | None = result.scalar_one_or_none()
        if competition:
            await self.db.delete(competition)
            await self.db.commit()
            return True
        return False

    async def get_competitions_between_dates(
        self, user_id: UUID4, start_month: date, end_month: date
    ):
        query = select(Competition).where(
            and_(
                Competition.user_id == user_id,
                Competition.start_date >= start_month,
                Competition.start_date <= end_month,
            )
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())
