from datetime import date

from pydantic import UUID4, BaseModel


class CompetitionViewSchema(BaseModel):
    id: UUID4
    start_date: date
    end_date: date

    class Config:
        from_attributes = True