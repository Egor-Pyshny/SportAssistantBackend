from datetime import date

from pydantic import BaseModel


class TrainingCampUpdateRequest(BaseModel):
    start_date: date
    end_date: date
    location: str
    notes: str
    goals: str
