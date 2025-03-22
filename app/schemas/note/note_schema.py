from datetime import date

from pydantic import UUID4, BaseModel


class NoteSchema(BaseModel):
    id: UUID4
    date: date
    text: str

    class Config:
        from_attributes = True
