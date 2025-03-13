from datetime import date

from pydantic import UUID4, BaseModel, Field


class TrainingCampDayUpdateRequest(BaseModel):
    id: UUID4 | None = Field(default=None)
    date: date
    goals: str
    notes: str
