from datetime import date
from typing import Annotated, List

from fastapi import APIRouter, Response, Body, Path, Query, Depends
from pydantic import UUID4

from constants.status_enum import CompetitionStatus
from constants.urls import Urls
from dependencies import authorized_only
from routers.training_camp.training_camp_service import TrainingCampService
from schemas.training_camp.training_camp_create_request import TrainingCampCreateRequest
from schemas.training_camp.training_camp_schema import TrainingCampSchema
from schemas.training_camp.training_camp_update_request import TrainingCampUpdateRequest
from schemas.training_camp_day.training_camp_day_schema import TrainingCampDaySchema
from schemas.training_camp_day.training_camp_update_request import TrainingCampDayUpdateRequest

training_camp_router = APIRouter()


@training_camp_router.post(path=Urls.camps_create.value)
async def create_camp(
    response: Response,
    body: Annotated[TrainingCampCreateRequest, Body()],
    sid: str | None = Depends(authorized_only),
    camp_service: TrainingCampService = Depends(TrainingCampService),
):
    response.set_cookie("sid", sid, httponly=True)
    await camp_service.create(body, sid)


@training_camp_router.get(path=Urls.competition_list.value, response_model=List[TrainingCampSchema])
async def get_camps(
    response: Response,
    sid: str | None = Depends(authorized_only),
    current_date: Annotated[date, Query()] = date.today(),
    status: Annotated[CompetitionStatus, Query()] = CompetitionStatus.current,
    camp_service: TrainingCampService = Depends(TrainingCampService),
):
    response.set_cookie("sid", sid, httponly=True)
    return await camp_service.get_all(sid=sid, current_date=current_date, status=status)


@training_camp_router.get(path=Urls.competition_days.value, response_model=List[TrainingCampDaySchema])
async def get_camp_days(
    response: Response,
    competition_id: UUID4,
    sid: str | None = Depends(authorized_only),
    camp_service: TrainingCampService = Depends(TrainingCampService),
):
    response.set_cookie("sid", sid, httponly=True)
    return await camp_service.get_all_days(competition_id)


@training_camp_router.get(path=Urls.competition_detail.value, response_model=TrainingCampSchema)
async def get_camp_info(
    response: Response,
    competition_id: Annotated[UUID4, Path()],
    sid: str | None = Depends(authorized_only),
    camp_service: TrainingCampService = Depends(TrainingCampService),
):
    response.set_cookie("sid", sid, httponly=True)
    return await camp_service.get_info(competition_id)


@training_camp_router.post(path=Urls.competition_update.value, response_model=TrainingCampSchema)
async def update_camp(
    response: Response,
    body: Annotated[TrainingCampUpdateRequest, Body()],
    competition_id: Annotated[UUID4, Path()],
    sid: str | None = Depends(authorized_only),
    camp_service: TrainingCampService = Depends(TrainingCampService),
):
    response.set_cookie("sid", sid, httponly=True)
    return await camp_service.update(competition_id, body)


@training_camp_router.delete(path=Urls.competition_delete.value)
async def delete_camp(
    response: Response,
    competition_id: Annotated[UUID4, Path()],
    sid: str | None = Depends(authorized_only),
    camp_service: TrainingCampService = Depends(TrainingCampService),
):
    response.set_cookie("sid", sid, httponly=True)
    return await camp_service.delete(competition_id)


@training_camp_router.get(path=Urls.competition_day.value)
async def get_camp_day(
    response: Response,
    competition_id: Annotated[UUID4, Path()],
    day: Annotated[date, Path()],
    sid: str | None = Depends(authorized_only),
    camp_service: TrainingCampService = Depends(TrainingCampService),
):
    response.set_cookie("sid", sid, httponly=True)
    return await camp_service.get_camp_day(competition_id, day)


@training_camp_router.post(path=Urls.competition_update_day.value)
async def update_camp_day(
    response: Response,
    competition_id: Annotated[UUID4, Path()],
    body: Annotated[TrainingCampDayUpdateRequest, Body()],
    sid: str | None = Depends(authorized_only),
    camp_service: TrainingCampService = Depends(TrainingCampService),
):
    response.set_cookie("sid", sid, httponly=True)
    return await camp_service.update_camp_day(competition_id, body)
