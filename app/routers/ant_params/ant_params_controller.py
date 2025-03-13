from typing import List, Annotated

from fastapi import APIRouter, Response, Depends, Body
from pydantic import UUID4

from constants.urls import Urls
from dependencies import authorized_only
from routers.ant_params.ant_params_service import AnthropometricParamsService
from schemas.ant_params.ant_params_create_request import AnthropometricParamsCreateRequest
from schemas.ant_params.ant_params_schema import AnthropometricParamsSchema
from schemas.ant_params.ant_params_update_request import AnthropometricParamsUpdateRequest
from schemas.ant_params.ant_params_view import AnthropometricParamsView

ant_params_router = APIRouter()


@ant_params_router.post(path=Urls.ant_params_create.value)
async def create_ant_params_result(
    response: Response,
    body: Annotated[AnthropometricParamsCreateRequest, Body()],
    sid: str | None = Depends(authorized_only),
    ant_params_service: AnthropometricParamsService = Depends(AnthropometricParamsService),
):
    response.set_cookie("sid", sid, httponly=True)
    await ant_params_service.create(body, sid)


@ant_params_router.get(path=Urls.ant_params_list.value, response_model=List[AnthropometricParamsView])
async def get_all(
    response: Response,
    sid: str | None = Depends(authorized_only),
    ant_params_service: AnthropometricParamsService = Depends(AnthropometricParamsService),
):
    response.set_cookie("sid", sid, httponly=True)
    return await ant_params_service.get_all(sid)


@ant_params_router.get(path=Urls.ant_params_detail.value, response_model=AnthropometricParamsSchema)
async def get(
    response: Response,
    params_id: UUID4,
    sid: str | None = Depends(authorized_only),
    ant_params_service: AnthropometricParamsService = Depends(AnthropometricParamsService),
):
    response.set_cookie("sid", sid, httponly=True)
    return await ant_params_service.get(params_id)


@ant_params_router.delete(path=Urls.ant_params_delete.value)
async def ant_params_delete(
    response: Response,
    params_id: UUID4,
    sid: str | None = Depends(authorized_only),
    ant_params_service: AnthropometricParamsService = Depends(AnthropometricParamsService),
):
    response.set_cookie("sid", sid, httponly=True)
    return await ant_params_service.delete(params_id)


@ant_params_router.post(path=Urls.ant_params_update.value, response_model=AnthropometricParamsSchema)
async def update_ant_params_result(
    response: Response,
    body: Annotated[AnthropometricParamsUpdateRequest, Body()],
    params_id: UUID4,
    sid: str | None = Depends(authorized_only),
    ant_params_service: AnthropometricParamsService = Depends(AnthropometricParamsService),
):
    response.set_cookie("sid", sid, httponly=True)
    return await ant_params_service.update(body, params_id)
