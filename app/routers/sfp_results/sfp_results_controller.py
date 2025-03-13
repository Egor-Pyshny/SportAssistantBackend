from typing import List, Annotated

from fastapi import APIRouter, Response, Depends, Body
from pydantic import UUID4

from constants.urls import Urls
from dependencies import authorized_only
from routers.sfp_results.sfp_results_service import SFPResultsService
from schemas.general.category_schema import CategorySchema
from schemas.sfp_results.sfp_result_create_request import SFPResultCreateRequest
from schemas.sfp_results.sfp_result_schema import SFPResultSchema
from schemas.sfp_results.sfp_result_update_request import SFPResultUpdateRequest
from schemas.sfp_results.sfp_results_view import SFPResultModelSchema

sfp_results_router = APIRouter()


@sfp_results_router.get(path=Urls.sfp_all_categories.value, response_model=List[CategorySchema])
async def get_all_categories(
    response: Response,
    sid: str | None = Depends(authorized_only),
    sfp_results_service: SFPResultsService = Depends(SFPResultsService),
):
    response.set_cookie("sid", sid, httponly=True)
    return await sfp_results_service.get_categories()


@sfp_results_router.post(path=Urls.sfp_create.value)
async def create_sfp_result(
    response: Response,
    body: Annotated[SFPResultCreateRequest, Body()],
    sid: str | None = Depends(authorized_only),
    sfp_results_service: SFPResultsService = Depends(SFPResultsService),
):
    response.set_cookie("sid", sid, httponly=True)
    await sfp_results_service.create(body, sid)


@sfp_results_router.get(path=Urls.sfp_list.value, response_model=List[SFPResultModelSchema])
async def get_all(
    response: Response,
    sid: str | None = Depends(authorized_only),
    sfp_results_service: SFPResultsService = Depends(SFPResultsService),
):
    response.set_cookie("sid", sid, httponly=True)
    return await sfp_results_service.get_all(sid)


@sfp_results_router.get(path=Urls.sfp_detail.value, response_model=SFPResultSchema)
async def get(
    response: Response,
    sfp_id: UUID4,
    sid: str | None = Depends(authorized_only),
    sfp_results_service: SFPResultsService = Depends(SFPResultsService),
):
    response.set_cookie("sid", sid, httponly=True)
    return await sfp_results_service.get(sfp_id)


@sfp_results_router.delete(path=Urls.sfp_delete.value)
async def sfp_delete(
    response: Response,
    sfp_id: UUID4,
    sid: str | None = Depends(authorized_only),
    sfp_results_service: SFPResultsService = Depends(SFPResultsService),
):
    response.set_cookie("sid", sid, httponly=True)
    return await sfp_results_service.delete(sfp_id)


@sfp_results_router.post(path=Urls.sfp_update.value, response_model=SFPResultSchema)
async def update_sfp_result(
    response: Response,
    body: Annotated[SFPResultUpdateRequest, Body()],
    sfp_id: UUID4,
    sid: str | None = Depends(authorized_only),
    sfp_results_service: SFPResultsService = Depends(SFPResultsService),
):
    response.set_cookie("sid", sid, httponly=True)
    return await sfp_results_service.update(body, sfp_id)
