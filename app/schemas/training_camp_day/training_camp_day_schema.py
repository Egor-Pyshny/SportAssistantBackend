from datetime import date

from pydantic import UUID4, BaseModel


class TrainingCampDaySchema(BaseModel):
    id: UUID4 | None
    camp_start_date: date
    camp_end_date: date
    camp_location: str
    date: date
    goals: str
    notes: str

    class Config:
        from_attributes = True
