from datetime import date

from pydantic import UUID4, BaseModel


class SFPResultUpdateRequest(BaseModel):
    sfp_category_id: UUID4
    date: date
    result: float
    notes: str
    goals: str
