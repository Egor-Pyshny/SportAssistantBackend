from typing import Annotated, List

from constants.urls import Urls
from dependencies import authorized_only
from fastapi import APIRouter, Body, Depends, Response
from pydantic import UUID4
from routers.note.note_service import NoteService
from schemas.note.note_create_request import NoteCreateRequest
from schemas.note.note_schema import NoteSchema
from schemas.note.note_update_request import NoteUpdateRequest
from schemas.note.note_view_schema import NoteViewSchema

notes_router = APIRouter()


@notes_router.post(path=Urls.note_create.value)
async def create_note_result(
    response: Response,
    body: Annotated[NoteCreateRequest, Body()],
    sid: str | None = Depends(authorized_only),
    notes_service: NoteService = Depends(NoteService),
):
    response.set_cookie("sid", sid, httponly=True)
    await notes_service.create(body, sid)


@notes_router.get(path=Urls.note_list.value, response_model=List[NoteViewSchema])
async def get_all(
    response: Response,
    sid: str | None = Depends(authorized_only),
    notes_service: NoteService = Depends(NoteService),
):
    response.set_cookie("sid", sid, httponly=True)
    return await notes_service.get_all(sid)


@notes_router.get(path=Urls.note_detail.value, response_model=NoteSchema)
async def get(
    response: Response,
    note_id: UUID4,
    sid: str | None = Depends(authorized_only),
    notes_service: NoteService = Depends(NoteService),
):
    response.set_cookie("sid", sid, httponly=True)
    return await notes_service.get(note_id)


@notes_router.delete(path=Urls.note_delete.value)
async def note_delete(
    response: Response,
    note_id: UUID4,
    sid: str | None = Depends(authorized_only),
    notes_service: NoteService = Depends(NoteService),
):
    response.set_cookie("sid", sid, httponly=True)
    return await notes_service.delete(note_id)


@notes_router.post(path=Urls.note_update.value, response_model=NoteSchema)
async def update_note(
    response: Response,
    body: Annotated[NoteUpdateRequest, Body()],
    note_id: UUID4,
    sid: str | None = Depends(authorized_only),
    notes_service: NoteService = Depends(NoteService),
):
    response.set_cookie("sid", sid, httponly=True)
    return await notes_service.update(body, note_id)
