from datetime import date

from pydantic import BaseModel

class CompetitionUpdateRequest(BaseModel):
    start_date: date
    end_date: date
    location: str
    notes: str
    name: str