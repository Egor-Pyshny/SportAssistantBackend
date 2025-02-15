from typing import Annotated

from constants.urls import Urls
from fastapi import APIRouter, Body, Request, Response, status
from fastapi.params import Cookie, Depends
from routers.auth.auth_service import AuthService
from routers.reponse_schemas.auth_responses import (
    forgot_password_responses,
    login_responses,
    registration_responses,
    resend_code_responses,
    reset_password_responses,
    verification_responses,
)
from schemas.auth.email_validation_request import EmailValidationRequest
from schemas.auth.forgot_password_request import ForgotPasswordRequest
from schemas.auth.login_request import LoginRequest
from schemas.auth.registration_request import RegistrationRequest
from schemas.auth.resend_request import ResendRequest
from schemas.auth.reset_password_request import ResetPasswordRequest
from slowapi import Limiter
from slowapi.util import get_remote_address

auth_router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@auth_router.post(path=Urls.login.value, responses=login_responses)
async def login(
    request: Annotated[LoginRequest, Body()],
    response: Response,
    auth_service: AuthService = Depends(AuthService),
):
    sid = await auth_service.login(request)
    response.set_cookie(key="sid", value=sid, httponly=True)


@auth_router.post(path=Urls.registration.value, responses=registration_responses)
async def registration(
    request: Annotated[RegistrationRequest, Body()],
    auth_service: AuthService = Depends(AuthService),
):
    await auth_service.registration(request)


@auth_router.post(
    path=Urls.verify_email.value,
    status_code=status.HTTP_201_CREATED,
    responses=verification_responses,
)
@limiter.limit("10/minute")
async def verify_email(
    request: Request,
    body: Annotated[EmailValidationRequest, Body()],
    response: Response,
    auth_service: AuthService = Depends(AuthService),
):
    sid = await auth_service.verify_email(body)
    response.set_cookie(key="sid", value=sid, httponly=True)


@auth_router.post(path=Urls.logout.value)
async def logout(
    response: Response,
    sid: str | None = Cookie(default=None),
    auth_service: AuthService = Depends(AuthService),
):
    await auth_service.logout(sid)
    response.delete_cookie(key="sid")


@auth_router.post(path=Urls.resend_verification_code.value, responses=resend_code_responses)
@limiter.limit("1/minute")
async def resend_code(
    request: Request,
    body: Annotated[ResendRequest, Body()],
    auth_service: AuthService = Depends(AuthService),
):
    await auth_service.resend_verification_code(body)


@auth_router.post(path=Urls.forgot_password.value, responses=forgot_password_responses)
@limiter.limit("1/minute")
async def forgot_password(
    request: Request,
    body: Annotated[ForgotPasswordRequest, Body()],
    auth_service: AuthService = Depends(AuthService),
):
    await auth_service.forgot_password(body)


@auth_router.post(path=Urls.reset_password.value, responses=reset_password_responses)
async def reset_password(
    request: Request,
    body: Annotated[ResetPasswordRequest, Body()],
    auth_service: AuthService = Depends(AuthService),
):
    await auth_service.reset_password(body)
