from typing import Annotated, List

from constants.urls import Urls
from dependencies import authorized_only
from fastapi import APIRouter, Body, Depends, Response
from pydantic import UUID4
from routers.comprehensive_examination.comprehensive_examination_service import (
    ComprehensiveExaminationService,
)
from schemas.comprehensive_examination.comprehensive_examination_create_schema import (
    ComprehensiveExaminationCreateRequests,
)
from schemas.comprehensive_examination.comprehensive_examination_schema import (
    ComprehensiveExaminationSchema,
)
from schemas.comprehensive_examination.comprehensive_examination_update_schema import (
    ComprehensiveExaminationUpdateRequest,
)
from schemas.comprehensive_examination.comprehensive_examination_view_schema import (
    ComprehensiveExaminationViewSchema,
)

comprehensive_exams_router = APIRouter()


@comprehensive_exams_router.post(path=Urls.comprehensive_examination_create.value)
async def create_comprehensive_exam_result(
    response: Response,
    body: Annotated[ComprehensiveExaminationCreateRequests, Body()],
    sid: str | None = Depends(authorized_only),
    comprehensive_exams_service: ComprehensiveExaminationService = Depends(
        ComprehensiveExaminationService
    ),
):
    response.set_cookie("sid", sid, httponly=True)
    await comprehensive_exams_service.create(body, sid)


@comprehensive_exams_router.get(
    path=Urls.comprehensive_examination_list.value,
    response_model=List[ComprehensiveExaminationViewSchema],
)
async def get_all(
    response: Response,
    sid: str | None = Depends(authorized_only),
    comprehensive_exams_service: ComprehensiveExaminationService = Depends(
        ComprehensiveExaminationService
    ),
):
    response.set_cookie("sid", sid, httponly=True)
    return await comprehensive_exams_service.get_all(sid)


@comprehensive_exams_router.get(
    path=Urls.comprehensive_examination_detail.value, response_model=ComprehensiveExaminationSchema
)
async def get(
    response: Response,
    exam_id: UUID4,
    sid: str | None = Depends(authorized_only),
    comprehensive_exams_service: ComprehensiveExaminationService = Depends(
        ComprehensiveExaminationService
    ),
):
    response.set_cookie("sid", sid, httponly=True)
    return await comprehensive_exams_service.get(exam_id)


@comprehensive_exams_router.delete(path=Urls.comprehensive_examination_delete.value)
async def comprehensive_exam_delete(
    response: Response,
    exam_id: UUID4,
    sid: str | None = Depends(authorized_only),
    comprehensive_exams_service: ComprehensiveExaminationService = Depends(
        ComprehensiveExaminationService
    ),
):
    response.set_cookie("sid", sid, httponly=True)
    return await comprehensive_exams_service.delete(exam_id)


@comprehensive_exams_router.post(
    path=Urls.comprehensive_examination_update.value, response_model=ComprehensiveExaminationSchema
)
async def update_comprehensive_exam_result(
    response: Response,
    body: Annotated[ComprehensiveExaminationUpdateRequest, Body()],
    exam_id: UUID4,
    sid: str | None = Depends(authorized_only),
    comprehensive_exams_service: ComprehensiveExaminationService = Depends(
        ComprehensiveExaminationService
    ),
):
    response.set_cookie("sid", sid, httponly=True)
    return await comprehensive_exams_service.update(body, exam_id)
