from datetime import date

from models import ComprehensiveExamination
from pydantic import UUID4
from schemas.comprehensive_examination.comprehensive_examination_update_schema import (
    ComprehensiveExaminationUpdateRequest,
)
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession


class ComprehensiveExaminationRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, exam: ComprehensiveExamination) -> ComprehensiveExamination:
        self.db.add(exam)
        await self.db.commit()
        await self.db.refresh(exam)
        return exam

    async def get_all(self, id: UUID4):
        query = select(ComprehensiveExamination).where(ComprehensiveExamination.user_id == id)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def delete(self, params_id: UUID4):
        query = select(ComprehensiveExamination).where(ComprehensiveExamination.id == params_id)
        result = await self.db.execute(query)
        exam: ComprehensiveExamination | None = result.scalar_one_or_none()
        if exam:
            await self.db.delete(exam)
            await self.db.commit()
            return True
        return False

    async def update(self, body: ComprehensiveExaminationUpdateRequest, params_id: UUID4):
        query = select(ComprehensiveExamination).where(ComprehensiveExamination.id == params_id)
        result = await self.db.execute(query)
        exam: ComprehensiveExamination | None = result.scalar_one_or_none()
        if exam:
            exam.date = body.date
            exam.methods = body.methods
            exam.institution = body.institution
            exam.recommendations = body.recommendations
            exam.specialists = body.specialists
            self.db.add(exam)
            await self.db.commit()
            await self.db.refresh(exam)
            return exam
        return None

    async def get(self, exam_id):
        query = select(ComprehensiveExamination).where(ComprehensiveExamination.id == exam_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_examinations_between_dates(
        self, user_id: UUID4, start_month: date, end_month: date
    ):
        query = select(ComprehensiveExamination).where(
            and_(
                ComprehensiveExamination.user_id == user_id,
                ComprehensiveExamination.date >= start_month,
                ComprehensiveExamination.date <= end_month,
            )
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())
