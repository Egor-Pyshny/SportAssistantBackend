from typing import Annotated

from constants.urls import Urls
from dependencies import authorized_only
from fastapi import APIRouter, Response, Body
from fastapi.params import Depends
from routers.reponse_schemas.user_responses import get_me_responses, check_email_responses
from routers.user.user_service import UserService
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

@user_router.post(
    path=Urls.check_email.value, responses=check_email_responses
)
async def check_email(
    request: Annotated[CheckEmailRequest, Body()],
    user_service: UserService = Depends(UserService),
):
    await user_service.check_email(request.email)
