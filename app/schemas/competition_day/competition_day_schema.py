from datetime import date

from pydantic import UUID4, BaseModel


class CompetitionDaySchema(BaseModel):
    id: UUID4
    date: date
    results: str
    notes: str

    class Config:
        from_attributes = True
