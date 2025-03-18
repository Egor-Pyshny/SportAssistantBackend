from datetime import date

from pydantic import BaseModel, UUID4


class NoteSchema(BaseModel):
    id: UUID4
    date: date
    text: str

    class Config:
        from_attributes = True