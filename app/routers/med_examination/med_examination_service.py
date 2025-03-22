from constants.prefixes import Prefixes
from dependencies import async_get_db, get_redis_client
from fastapi import Depends, HTTPException
from models import MedExamination
from pydantic import UUID4
from repositories.med_examination.med_examination_repository import MedExaminationRepository
from schemas.auth.redis_session_data import RedisSessionData
from schemas.med_examination.med_examination_create_schema import MedExaminationCreateRequest
from schemas.med_examination.med_examination_schema import MedExaminationSchema
from schemas.med_examination.med_examination_update_schema import MedExaminationUpdateRequest
from schemas.med_examination.med_examination_view_schema import MedExaminationViewSchema
from services.redis import RedisClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status


class MedExaminationService:

    def __init__(
        self,
        db: AsyncSession = Depends(async_get_db),
        redis_client: RedisClient = Depends(get_redis_client),
    ):
        self.med_exams_repository: MedExaminationRepository = MedExaminationRepository(db)
        self.redis_client: RedisClient = redis_client

    async def create(self, body: MedExaminationCreateRequest, sid: str):
        dict = self.redis_client.get(f"{Prefixes.redis_session_prefix.value}:{sid}")
        user = RedisSessionData(**dict)
        await self.med_exams_repository.create(MedExamination(**body.model_dump(), user_id=user.id))

    async def get_all(self, sid: str):
        dict = self.redis_client.get(f"{Prefixes.redis_session_prefix.value}:{sid}")
        user = RedisSessionData(**dict)
        results = await self.med_exams_repository.get_all(user.id)
        results_schema = [MedExaminationViewSchema.model_validate(result) for result in results]
        return results_schema

    async def delete(self, exam_id: UUID4):
        res = await self.med_exams_repository.delete(exam_id)
        if not res:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="MedExamination not found"
            )

    async def update(self, body: MedExaminationUpdateRequest, exam_id: UUID4):
        new_result = await self.med_exams_repository.update(body, exam_id)
        if new_result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="MedExamination not found"
            )
        return MedExaminationSchema.model_validate(new_result)

    async def get(self, exam_id: UUID4):
        res = await self.med_exams_repository.get(exam_id)
        if res is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="MedExamination not found"
            )
        schema = MedExaminationSchema.model_validate(res)
        return schema
