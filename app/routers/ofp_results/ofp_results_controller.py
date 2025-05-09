from datetime import date
from typing import Annotated, List

from constants.urls import Urls
from dependencies import authorized_only
from fastapi import APIRouter, Body, Depends, Query, Response
from pydantic import UUID4
from routers.ofp_results.ofp_results_service import OFPResultsService
from schemas.general.category_schema import CategorySchema
from schemas.general.graphic_data import GraphicPoint
from schemas.ofp_results.ofp_result_create_request import OFPResultCreateRequest
from schemas.ofp_results.ofp_result_schema import OFPResultSchema
from schemas.ofp_results.ofp_result_update_request import OFPResultUpdateRequest
from schemas.ofp_results.ofp_results_view import OFPResultViewSchema

ofp_results_router = APIRouter()


@ofp_results_router.get(path=Urls.ofp_all_categories.value, response_model=List[CategorySchema])
async def get_all_categories(
    response: Response,
    sid: str | None = Depends(authorized_only),
    ofp_results_service: OFPResultsService = Depends(OFPResultsService),
):
    response.set_cookie("sid", sid, httponly=True)
    return await ofp_results_service.get_categories()


@ofp_results_router.post(path=Urls.ofp_create.value)
async def create_ofp_result(
    response: Response,
    body: Annotated[OFPResultCreateRequest, Body()],
    sid: str | None = Depends(authorized_only),
    ofp_results_service: OFPResultsService = Depends(OFPResultsService),
):
    response.set_cookie("sid", sid, httponly=True)
    await ofp_results_service.create(body, sid)


@ofp_results_router.get(path=Urls.ofp_list.value, response_model=List[OFPResultViewSchema])
async def get_all(
    response: Response,
    sid: str | None = Depends(authorized_only),
    ofp_results_service: OFPResultsService = Depends(OFPResultsService),
):
    response.set_cookie("sid", sid, httponly=True)
    return await ofp_results_service.get_all(sid)


@ofp_results_router.get(path=Urls.ofp_detail.value, response_model=OFPResultSchema)
async def get(
    response: Response,
    ofp_id: UUID4,
    sid: str | None = Depends(authorized_only),
    ofp_results_service: OFPResultsService = Depends(OFPResultsService),
):
    response.set_cookie("sid", sid, httponly=True)
    return await ofp_results_service.get(ofp_id)


@ofp_results_router.delete(path=Urls.ofp_delete.value)
async def ofp_delete(
    response: Response,
    ofp_id: UUID4,
    sid: str | None = Depends(authorized_only),
    ofp_results_service: OFPResultsService = Depends(OFPResultsService),
):
    response.set_cookie("sid", sid, httponly=True)
    return await ofp_results_service.delete(ofp_id)


@ofp_results_router.post(path=Urls.ofp_update.value, response_model=OFPResultSchema)
async def update_ofp_result(
    response: Response,
    body: Annotated[OFPResultUpdateRequest, Body()],
    ofp_id: UUID4,
    sid: str | None = Depends(authorized_only),
    ofp_results_service: OFPResultsService = Depends(OFPResultsService),
):
    response.set_cookie("sid", sid, httponly=True)
    return await ofp_results_service.update(body, ofp_id)


@ofp_results_router.get(path=Urls.ofp_get_graphic_data.value, response_model=List[GraphicPoint])
async def get_ofp_results_graphic_data(
    response: Response,
    start_date: Annotated[date, Query()],
    end_date: Annotated[date, Query()],
    category_id: Annotated[UUID4, Query()],
    sid: str | None = Depends(authorized_only),
    ofp_results_service: OFPResultsService = Depends(OFPResultsService),
):
    response.set_cookie("sid", sid, httponly=True)
    return await ofp_results_service.get_graphic_data(start_date, end_date, category_id, sid)
