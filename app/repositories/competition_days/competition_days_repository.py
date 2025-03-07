from models import CompetitionDay
from sqlalchemy.ext.asyncio import AsyncSession


class CompetitionDaysRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, new_competition_day: CompetitionDay) -> CompetitionDay:
        self.db.add(new_competition_day)
        await self.db.commit()
        await self.db.refresh(new_competition_day)
        return new_competition_day
