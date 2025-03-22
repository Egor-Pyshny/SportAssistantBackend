from constants.prefixes import Prefixes
from dependencies import async_get_db, get_redis_client
from fastapi import Depends, HTTPException
from models import ComprehensiveExamination
from pydantic import UUID4
from repositories.comprehensive_examination.comprehensive_examination_repository import (
    ComprehensiveExaminationRepository,
)
from schemas.auth.redis_session_data import RedisSessionData
from schemas.comprehensive_examination.comprehensive_examination_create_schema import (
    ComprehensiveExaminationCreateRequests,
)
from schemas.comprehensive_examination.comprehensive_examination_schema import (
    ComprehensiveExaminationSchema,
)
from schemas.comprehensive_examination.comprehensive_examination_update_schema import (
    ComprehensiveExaminationUpdateRequest,
)
from schemas.comprehensive_examination.comprehensive_examination_view_schema import (
    ComprehensiveExaminationViewSchema,
)
from services.redis import RedisClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status


class ComprehensiveExaminationService:

    def __init__(
        self,
        db: AsyncSession = Depends(async_get_db),
        redis_client: RedisClient = Depends(get_redis_client),
    ):
        self.comprehensive_exams_repository: ComprehensiveExaminationRepository = (
            ComprehensiveExaminationRepository(db)
        )
        self.redis_client: RedisClient = redis_client

    async def create(self, body: ComprehensiveExaminationCreateRequests, sid: str):
        dict = self.redis_client.get(f"{Prefixes.redis_session_prefix.value}:{sid}")
        user = RedisSessionData(**dict)
        await self.comprehensive_exams_repository.create(
            ComprehensiveExamination(**body.model_dump(), user_id=user.id)
        )

    async def get_all(self, sid: str):
        dict = self.redis_client.get(f"{Prefixes.redis_session_prefix.value}:{sid}")
        user = RedisSessionData(**dict)
        results = await self.comprehensive_exams_repository.get_all(user.id)
        results_schema = [
            ComprehensiveExaminationViewSchema.model_validate(result) for result in results
        ]
        return results_schema

    async def delete(self, exam_id: UUID4):
        res = await self.comprehensive_exams_repository.delete(exam_id)
        if not res:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="ComprehensiveExamination not found"
            )

    async def update(self, body: ComprehensiveExaminationUpdateRequest, exam_id: UUID4):
        new_result = await self.comprehensive_exams_repository.update(body, exam_id)
        if new_result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="ComprehensiveExamination not found"
            )
        return ComprehensiveExaminationSchema.model_validate(new_result)

    async def get(self, exam_id: UUID4):
        res = await self.comprehensive_exams_repository.get(exam_id)
        if res is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="ComprehensiveExamination not found"
            )
        schema = ComprehensiveExaminationSchema.model_validate(res)
        return schema
