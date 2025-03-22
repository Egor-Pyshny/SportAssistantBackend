from typing import Annotated, List

from constants.urls import Urls
from dependencies import authorized_only
from fastapi import APIRouter, Body, Depends, Response
from pydantic import UUID4
from routers.med_examination.med_examination_service import MedExaminationService
from schemas.med_examination.med_examination_create_schema import MedExaminationCreateRequest
from schemas.med_examination.med_examination_schema import MedExaminationSchema
from schemas.med_examination.med_examination_update_schema import MedExaminationUpdateRequest
from schemas.med_examination.med_examination_view_schema import MedExaminationViewSchema

med_exams_router = APIRouter()


@med_exams_router.post(path=Urls.med_examination_create.value)
async def create_med_exam_result(
    response: Response,
    body: Annotated[MedExaminationCreateRequest, Body()],
    sid: str | None = Depends(authorized_only),
    med_exams_service: MedExaminationService = Depends(MedExaminationService),
):
    response.set_cookie("sid", sid, httponly=True)
    await med_exams_service.create(body, sid)


@med_exams_router.get(
    path=Urls.med_examination_list.value, response_model=List[MedExaminationViewSchema]
)
async def get_all(
    response: Response,
    sid: str | None = Depends(authorized_only),
    med_exams_service: MedExaminationService = Depends(MedExaminationService),
):
    response.set_cookie("sid", sid, httponly=True)
    return await med_exams_service.get_all(sid)


@med_exams_router.get(path=Urls.med_examination_detail.value, response_model=MedExaminationSchema)
async def get(
    response: Response,
    exam_id: UUID4,
    sid: str | None = Depends(authorized_only),
    med_exams_service: MedExaminationService = Depends(MedExaminationService),
):
    response.set_cookie("sid", sid, httponly=True)
    return await med_exams_service.get(exam_id)


@med_exams_router.delete(path=Urls.med_examination_delete.value)
async def med_exam_delete(
    response: Response,
    exam_id: UUID4,
    sid: str | None = Depends(authorized_only),
    med_exams_service: MedExaminationService = Depends(MedExaminationService),
):
    response.set_cookie("sid", sid, httponly=True)
    return await med_exams_service.delete(exam_id)


@med_exams_router.post(path=Urls.med_examination_update.value, response_model=MedExaminationSchema)
async def update_med_exam_result(
    response: Response,
    body: Annotated[MedExaminationUpdateRequest, Body()],
    exam_id: UUID4,
    sid: str | None = Depends(authorized_only),
    med_exams_service: MedExaminationService = Depends(MedExaminationService),
):
    response.set_cookie("sid", sid, httponly=True)
    return await med_exams_service.update(body, exam_id)
