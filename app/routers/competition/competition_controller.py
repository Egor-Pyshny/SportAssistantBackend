from datetime import date
from typing import Annotated, List

from constants.status_enum import CompetitionStatus
from constants.urls import Urls
from dependencies import authorized_only
from fastapi import APIRouter, Body, Depends, Path, Query, Response
from pydantic import UUID4
from routers.competition.competition_service import CompetitionService
from schemas.competition.competition_create_request import CompetitionCreateRequest
from schemas.competition.competition_schema import CompetitionSchema
from schemas.competition.competition_update_request import CompetitionUpdateRequest
from schemas.competition_day.competition_day_schema import CompetitionDaySchema
from schemas.competition_day.competition_day_update_request import CompetitionDayUpdateRequest
from schemas.competition_result.competition_result_update_request import CompetitionResultUpdateRequest

competition_router = APIRouter()


@competition_router.post(path=Urls.competition_create.value)
async def create_competition(
    response: Response,
    body: Annotated[CompetitionCreateRequest, Body()],
    sid: str | None = Depends(authorized_only),
    competition_service: CompetitionService = Depends(CompetitionService),
):
    response.set_cookie("sid", sid, httponly=True)
    await competition_service.create(body, sid)


@competition_router.get(path=Urls.competition_list.value, response_model=List[CompetitionSchema])
async def get_competitions(
    response: Response,
    sid: str | None = Depends(authorized_only),
    current_date: Annotated[date, Query()] = date.today(),
    status: Annotated[CompetitionStatus, Query()] = CompetitionStatus.current,
    competition_service: CompetitionService = Depends(CompetitionService),
):
    response.set_cookie("sid", sid, httponly=True)
    return await competition_service.get_all(sid=sid, current_date=current_date, status=status)


@competition_router.get(path=Urls.competition_days.value, response_model=List[CompetitionDaySchema])
async def get_competition_days(
    response: Response,
    competition_id: UUID4,
    sid: str | None = Depends(authorized_only),
    competition_service: CompetitionService = Depends(CompetitionService),
):
    response.set_cookie("sid", sid, httponly=True)
    return await competition_service.get_all_days(competition_id)


@competition_router.get(path=Urls.competition_detail.value, response_model=CompetitionSchema)
async def get_competition_info(
    response: Response,
    competition_id: Annotated[UUID4, Path()],
    sid: str | None = Depends(authorized_only),
    competition_service: CompetitionService = Depends(CompetitionService),
):
    response.set_cookie("sid", sid, httponly=True)
    return await competition_service.get_info(competition_id)


@competition_router.post(path=Urls.competition_update.value, response_model=CompetitionSchema)
async def update_competition(
    response: Response,
    body: Annotated[CompetitionUpdateRequest, Body()],
    competition_id: Annotated[UUID4, Path()],
    sid: str | None = Depends(authorized_only),
    competition_service: CompetitionService = Depends(CompetitionService),
):
    response.set_cookie("sid", sid, httponly=True)
    return await competition_service.update(competition_id, body)


@competition_router.delete(path=Urls.competition_delete.value)
async def delete_competition(
    response: Response,
    competition_id: Annotated[UUID4, Path()],
    sid: str | None = Depends(authorized_only),
    competition_service: CompetitionService = Depends(CompetitionService),
):
    response.set_cookie("sid", sid, httponly=True)
    return await competition_service.delete(competition_id)


@competition_router.get(path=Urls.competition_day.value)
async def get_competition_day(
    response: Response,
    competition_id: Annotated[UUID4, Path()],
    day: Annotated[date, Path()],
    sid: str | None = Depends(authorized_only),
    competition_service: CompetitionService = Depends(CompetitionService),
):
    response.set_cookie("sid", sid, httponly=True)
    return await competition_service.get_competition_day(competition_id, day)


@competition_router.post(path=Urls.competition_update_day.value)
async def update_competition_day(
    response: Response,
    competition_id: Annotated[UUID4, Path()],
    body: Annotated[CompetitionDayUpdateRequest, Body()],
    sid: str | None = Depends(authorized_only),
    competition_service: CompetitionService = Depends(CompetitionService),
):
    response.set_cookie("sid", sid, httponly=True)
    return await competition_service.update_competition_day(competition_id, body)


@competition_router.get(path=Urls.competition_results.value)
async def get_competition_result(
    response: Response,
    competition_id: Annotated[UUID4, Path()],
    sid: str | None = Depends(authorized_only),
    competition_service: CompetitionService = Depends(CompetitionService),
):
    response.set_cookie("sid", sid, httponly=True)
    return await competition_service.get_competition_result(competition_id)


@competition_router.post(path=Urls.competition_update_result.value)
async def update_competition_result(
    response: Response,
    competition_id: Annotated[UUID4, Path()],
    body: Annotated[CompetitionResultUpdateRequest, Body()],
    sid: str | None = Depends(authorized_only),
    competition_service: CompetitionService = Depends(CompetitionService),
):
    response.set_cookie("sid", sid, httponly=True)
    return await competition_service.update_competition_result(competition_id, body)
