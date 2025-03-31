from datetime import date

from models import Note
from pydantic import UUID4
from schemas.note.note_update_request import NoteUpdateRequest
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession


class NotesRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, result: Note) -> Note:
        self.db.add(result)
        await self.db.commit()
        await self.db.refresh(result)
        return result

    async def get_all(self, id: UUID4):
        query = select(Note).where(Note.user_id == id)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def delete(self, note_id: UUID4):
        query = select(Note).where(Note.id == note_id)
        result = await self.db.execute(query)
        note: Note | None = result.scalar_one_or_none()
        if note:
            await self.db.delete(note)
            await self.db.commit()
            return True
        return False

    async def update(self, body: NoteUpdateRequest, note_id: UUID4):
        query = select(Note).where(Note.id == note_id)
        result = await self.db.execute(query)
        note: Note | None = result.scalar_one_or_none()
        if result:
            note.text = body.text
            self.db.add(note)
            await self.db.commit()
            await self.db.refresh(note)
            return note
        return None

    async def get(self, note_id):
        query = select(Note).where(Note.id == note_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_date(self, user_id: UUID4, current_date: date):
        query = select(Note).where(
            and_(
                Note.user_id == user_id,
                Note.date == current_date,
            )
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_notes_between_dates(self, user_id: UUID4, start_month: date, end_month: date):
        query = select(Note).where(
            and_(
                Note.user_id == user_id,
                Note.date >= start_month,
                Note.date <= end_month,
            )
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())
