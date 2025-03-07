from datetime import date

from pydantic import UUID4, BaseModel


class CompetitionSchema(BaseModel):
    id: UUID4
    start_date: date
    end_date: date
    location: str
    notes: str
    name: str

    class Config:
        from_attributes = True
