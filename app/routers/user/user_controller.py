from typing import Annotated

from constants.urls import Urls
from dependencies import authorized_only
from fastapi import APIRouter, Body, Response
from fastapi.params import Depends
from routers.reponse_schemas.user_responses import check_email_responses, get_me_responses
from routers.user.user_service import UserService
from schemas.user.set_profile_info_request import SetProfileInfoRequest
from schemas.user.user_check_email_request import CheckEmailRequest
from schemas.user.user_response_schema import UserResponseSchema

user_router = APIRouter()


@user_router.get(
    path=Urls.get_me.value, response_model=UserResponseSchema, responses=get_me_responses
)
async def get_me(
    response: Response,
    sid: str | None = Depends(authorized_only),
    user_service: UserService = Depends(UserService),
):
    response.set_cookie("sid", sid, httponly=True)
    res = await user_service.get_me(sid)
    return res


@user_router.get(path=Urls.is_profile_filled.value)
async def check_profile_info(
    response: Response,
    sid: str | None = Depends(authorized_only),
    user_service: UserService = Depends(UserService),
):
    response.set_cookie("sid", sid, httponly=True)
    return await user_service.is_profile_filled(sid)


@user_router.post(path=Urls.set_info.value)
async def set_info(
    response: Response,
    request: Annotated[SetProfileInfoRequest, Body()],
    sid: str | None = Depends(authorized_only),
    user_service: UserService = Depends(UserService),
):
    response.set_cookie("sid", sid, httponly=True)
    await user_service.set_info(sid, request)


@user_router.post(path=Urls.check_email.value, responses=check_email_responses)
async def check_email(
    request: Annotated[CheckEmailRequest, Body()],
    user_service: UserService = Depends(UserService),
):
    await user_service.check_email(request.email)
