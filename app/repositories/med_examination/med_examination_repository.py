from datetime import date

from models import MedExamination
from pydantic import UUID4
from schemas.med_examination.med_examination_update_schema import MedExaminationUpdateRequest
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession


class MedExaminationRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, exam: MedExamination) -> MedExamination:
        self.db.add(exam)
        await self.db.commit()
        await self.db.refresh(exam)
        return exam

    async def get_all(self, id: UUID4):
        query = select(MedExamination).where(MedExamination.user_id == id)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def delete(self, params_id: UUID4):
        query = select(MedExamination).where(MedExamination.id == params_id)
        result = await self.db.execute(query)
        exam: MedExamination | None = result.scalar_one_or_none()
        if exam:
            await self.db.delete(exam)
            await self.db.commit()
            return True
        return False

    async def update(self, body: MedExaminationUpdateRequest, params_id: UUID4):
        query = select(MedExamination).where(MedExamination.id == params_id)
        result = await self.db.execute(query)
        exam: MedExamination | None = result.scalar_one_or_none()
        if exam:
            exam.date = body.date
            exam.methods = body.methods
            exam.institution = body.institution
            exam.recommendations = body.recommendations
            self.db.add(exam)
            await self.db.commit()
            await self.db.refresh(exam)
            return exam
        return None

    async def get(self, exam_id):
        query = select(MedExamination).where(MedExamination.id == exam_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_examinations_between_dates(
        self, user_id: UUID4, start_month: date, end_month: date
    ):
        query = select(MedExamination).where(
            and_(
                MedExamination.user_id == user_id,
                MedExamination.date >= start_month,
                MedExamination.date <= end_month,
            )
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())
