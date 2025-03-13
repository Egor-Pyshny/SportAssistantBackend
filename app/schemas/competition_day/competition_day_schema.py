from datetime import date

from pydantic import UUID4, BaseModel


class CompetitionDaySchema(BaseModel):
    id: UUID4 | None
    date: date
    competition_start_date: date
    competition_end_date: date
    competition_location: str
    competition_name: str
    results: str
    notes: str

    class Config:
        from_attributes = True
