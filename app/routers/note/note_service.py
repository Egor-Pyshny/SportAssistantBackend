from constants.prefixes import Prefixes
from dependencies import async_get_db, get_redis_client
from fastapi import Depends, HTTPException
from models import Note
from pydantic import UUID4
from repositories.notes.notes_repository import NotesRepository
from schemas.auth.redis_session_data import RedisSessionData
from schemas.note.note_create_request import NoteCreateRequest
from schemas.note.note_schema import NoteSchema
from schemas.note.note_update_request import NoteUpdateRequest
from schemas.note.note_view_schema import NoteViewSchema
from services.redis import RedisClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status


class NoteService:

    def __init__(
        self,
        db: AsyncSession = Depends(async_get_db),
        redis_client: RedisClient = Depends(get_redis_client),
    ):
        self.notes_repository: NotesRepository = NotesRepository(db)
        self.redis_client: RedisClient = redis_client

    async def create(self, body: NoteCreateRequest, sid: str):
        dict = self.redis_client.get(f"{Prefixes.redis_session_prefix.value}:{sid}")
        user = RedisSessionData(**dict)
        await self.notes_repository.create(Note(**body.model_dump(), user_id=user.id))

    async def get_all(self, sid: str):
        dict = self.redis_client.get(f"{Prefixes.redis_session_prefix.value}:{sid}")
        user = RedisSessionData(**dict)
        notes = await self.notes_repository.get_all(user.id)
        notes_schema = [NoteViewSchema.model_validate(note) for note in notes]
        return notes_schema

    async def delete(self, note_id: UUID4):
        res = await self.notes_repository.delete(note_id)
        if not res:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

    async def update(self, body: NoteUpdateRequest, note_id: UUID4):
        new_schema = await self.notes_repository.update(body, note_id)
        if new_schema is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
        return NoteSchema.model_validate(new_schema)

    async def get(self, note_id: UUID4):
        res = await self.notes_repository.get(note_id)
        if res is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
        schema = NoteSchema.model_validate(res)
        return schema
