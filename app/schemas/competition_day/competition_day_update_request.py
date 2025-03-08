from datetime import date

from pydantic import UUID4, BaseModel, Field


class CompetitionDayUpdateRequest(BaseModel):
    id: UUID4 | None = Field(default=None)
    date: date
    result: str
    notes: str
