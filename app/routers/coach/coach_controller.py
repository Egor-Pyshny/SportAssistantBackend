from typing import List

from constants.urls import Urls
from fastapi import APIRouter, Depends
from pydantic import UUID4
from routers.coach.coach_service import CoachService
from schemas.coach.coach_schema import CoachSchema

coach_router = APIRouter()


@coach_router.get(path=Urls.coach_detail.value, response_model=CoachSchema)
async def get_coach(coach_id: UUID4, coach_service: CoachService = Depends(CoachService)):
    return await coach_service.get_by_id(coach_id)


@coach_router.get(path=Urls.coach_list.value, response_model=List[CoachSchema])
async def get_all_coaches(coach_service: CoachService = Depends(CoachService)):
    return await coach_service.get_all()
