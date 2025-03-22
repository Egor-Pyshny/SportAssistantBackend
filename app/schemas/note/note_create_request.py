from datetime import date

from pydantic import BaseModel


class NoteCreateRequest(BaseModel):
    date: date
    text: str
