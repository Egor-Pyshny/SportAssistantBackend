import datetime
from datetime import date

from models import CompetitionDay
from pydantic import UUID4
from schemas.competition_day.competition_day_update_request import CompetitionDayUpdateRequest
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession


class CompetitionDaysRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, new_competition_day: CompetitionDay) -> CompetitionDay:
        self.db.add(new_competition_day)
        await self.db.commit()
        await self.db.refresh(new_competition_day)
        return new_competition_day

    async def get_day(self, competition_id: UUID4, day: date):
        query = select(CompetitionDay).where(
            and_(CompetitionDay.competition_id == competition_id, CompetitionDay.date == day)
        )
        result = await self.db.execute(query)
        competition: CompetitionDay | None = result.scalar_one_or_none()
        return competition

    async def update(self, competition_id: UUID4, data: CompetitionDayUpdateRequest):
        query = select(CompetitionDay).where(
            and_(CompetitionDay.competition_id == competition_id, CompetitionDay.date == data.date)
        )
        result = await self.db.execute(query)
        competition_day: CompetitionDay | None = result.scalar_one_or_none()
        if competition_day:
            competition_day.notes = data.notes
            competition_day.results = data.result
            self.db.add(competition_day)
            await self.db.commit()
            await self.db.refresh(competition_day)
            return competition_day
        return None
