from datetime import date

from pydantic import UUID4, BaseModel


class TrainingCampSchema(BaseModel):
    id: UUID4
    start_date: date
    end_date: date
    location: str
    notes: str
    goals: str

    class Config:
        from_attributes = True
