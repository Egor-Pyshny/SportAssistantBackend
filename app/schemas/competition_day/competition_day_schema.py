from datetime import date

from pydantic import UUID4, BaseModel


class CompetitionDaySchema(BaseModel):
    id: UUID4 | None
    competition_name: str
    competition_start_date: date
    competition_end_date: date
    competition_location: str
    date: date
    results: str
    notes: str

    class Config:
        from_attributes = True
