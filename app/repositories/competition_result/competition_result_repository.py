from datetime import date

from models import CompetitionDay, CompetitionResult
from pydantic import UUID4
from schemas.competition_day.competition_day_update_request import CompetitionDayUpdateRequest
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.competition_result.competition_result_update_request import CompetitionResultUpdateRequest


class CompetitionResultRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, new_competition_result: CompetitionResult) -> CompetitionResult:
        self.db.add(new_competition_result)
        await self.db.commit()
        await self.db.refresh(new_competition_result)
        return new_competition_result

    async def get(self, competition_id: UUID4):
        query = select(CompetitionResult).where(CompetitionResult.competition_id == competition_id)
        result = await self.db.execute(query)
        competition: CompetitionResult | None = result.scalar_one_or_none()
        return competition

    async def update(self, competition_id: UUID4, data: CompetitionResultUpdateRequest):
        query = select(CompetitionResult).where(CompetitionResult.competition_id == competition_id)
        result = await self.db.execute(query)
        competition_result: CompetitionResult | None = result.scalar_one_or_none()
        if competition_result:
            competition_result.notes = data.notes
            competition_result.results = data.result
            self.db.add(competition_result)
            await self.db.commit()
            await self.db.refresh(competition_result)
            return competition_result
        return None
