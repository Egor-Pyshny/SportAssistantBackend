from datetime import date
from typing import List

from models import OFPCategory, OFPResults
from pydantic import UUID4
from schemas.ofp_results.ofp_result_update_request import OFPResultUpdateRequest
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import subqueryload


class OFPResultsRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_categories(self):
        query = select(OFPCategory)
        result = await self.db.execute(query)
        categories: List[OFPCategory] = list(result.scalars().all())
        return categories

    async def create(self, result: OFPResults) -> OFPResults:
        self.db.add(result)
        await self.db.commit()
        await self.db.refresh(result)
        return result

    async def get_all(self, id: UUID4):
        query = (
            select(OFPResults)
            .options(subqueryload(OFPResults.ofp_category))
            .where(OFPResults.user_id == id)
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def delete(self, ofp_id: UUID4):
        query = select(OFPResults).where(OFPResults.id == ofp_id)
        result = await self.db.execute(query)
        result: OFPResults | None = result.scalar_one_or_none()
        if result:
            await self.db.delete(result)
            await self.db.commit()
            return True
        return False

    async def update(self, body: OFPResultUpdateRequest, ofp_id: UUID4):
        query = (
            select(OFPResults)
            .options(subqueryload(OFPResults.ofp_category))
            .where(OFPResults.id == ofp_id)
        )
        result = await self.db.execute(query)
        result: OFPResults | None = result.scalar_one_or_none()
        if result:
            result.ofp_category_id = body.ofp_category_id
            result.date = body.date
            result.goals = body.goals
            result.result = body.result
            result.notes = body.notes
            self.db.add(result)
            await self.db.commit()
            await self.db.refresh(result)
            return result
        return None

    async def get(self, ofp_id):
        query = select(OFPResults).where(OFPResults.id == ofp_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_graphic_data(
        self, start_date: date, end_date: date, category_id: UUID4, user_id: UUID4
    ):
        query = select(OFPResults).where(
            and_(
                OFPResults.user_id == user_id,
                OFPResults.date >= start_date,
                OFPResults.date <= end_date,
                OFPResults.ofp_category_id == category_id,
            )
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_examinations_between_dates(
        self, user_id: UUID4, start_month: date, end_month: date
    ):
        query = (
            select(OFPResults)
            .options(subqueryload(OFPResults.ofp_category))
            .where(
                and_(
                    OFPResults.user_id == user_id,
                    OFPResults.date >= start_month,
                    OFPResults.date <= end_month,
                )
            )
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())
