from datetime import date

from pydantic import UUID4, BaseModel


class CompetitionResultSchema(BaseModel):
    id: UUID4 | None
    results: str
    notes: str

    class Config:
        from_attributes = True
