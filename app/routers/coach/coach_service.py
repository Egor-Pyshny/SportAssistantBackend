from dependencies import async_get_db
from fastapi import HTTPException, status
from fastapi.params import Depends
from pydantic import UUID4
from repositories.coach.coach_repository import CoachRepository
from schemas.coach.coach_schema import CoachSchema
from sqlalchemy.ext.asyncio import AsyncSession


class CoachService:

    def __init__(
        self,
        db: AsyncSession = Depends(async_get_db),
    ):
        self.coach_repository: CoachRepository = CoachRepository(db)

    async def get_all(self):
        coaches = await self.coach_repository.get_all()
        coaches_schemas = [CoachSchema.model_validate(coach) for coach in coaches]
        return coaches_schemas

    async def get_by_id(self, id: UUID4):
        coach = await self.coach_repository.get(id)
        if coach is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Coach not found")
        return CoachSchema.model_validate(coach)
