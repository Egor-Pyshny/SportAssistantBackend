from pydantic import BaseModel


class NoteUpdateRequest(BaseModel):
    text: str