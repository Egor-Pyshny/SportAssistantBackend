from datetime import date
from typing import List

from pydantic import UUID4
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import subqueryload

from models import SFPCategory, SFPResults
from schemas.sfp_results.sfp_result_update_request import SFPResultUpdateRequest


class SFPResultsRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_categories(self):
        query = select(SFPCategory)
        result = await self.db.execute(query)
        categories: List[SFPCategory] = list(result.scalars().all())
        return categories

    async def create(self, result: SFPResults) -> SFPResults:
        self.db.add(result)
        await self.db.commit()
        await self.db.refresh(result)
        return result

    async def get_all(self, id: UUID4):
        query = select(SFPResults).options(subqueryload(SFPResults.sfp_category)).where(SFPResults.user_id == id)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def delete(self, sfp_id: UUID4):
        query = select(SFPResults).where(SFPResults.id == sfp_id)
        result = await self.db.execute(query)
        result: SFPResults | None = result.scalar_one_or_none()
        if result:
            await self.db.delete(result)
            await self.db.commit()
            return True
        return False

    async def update(self, body: SFPResultUpdateRequest, sfp_id: UUID4):
        query = select(SFPResults).options(subqueryload(SFPResults.sfp_category)).where(SFPResults.id == sfp_id)
        result = await self.db.execute(query)
        result: SFPResults | None = result.scalar_one_or_none()
        if result:
            result.sfp_category_id = body.sfp_category_id
            result.date = body.date
            result.goals = body.goals
            result.result = body.result
            result.notes = body.notes
            self.db.add(result)
            await self.db.commit()
            await self.db.refresh(result)
            return result
        return None

    async def get(self, sfp_id):
        query = select(SFPResults).where(SFPResults.id == sfp_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_graphic_data(self, start_date: date, end_date: date, category_id: UUID4, user_id: UUID4):
        query = select(SFPResults).where(
            and_(
                SFPResults.user_id == user_id,
                SFPResults.date >= start_date,
                SFPResults.date <= end_date,
                SFPResults.sfp_category_id == category_id
            )
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())
