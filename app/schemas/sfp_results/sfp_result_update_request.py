from datetime import date

from pydantic import BaseModel, UUID4


class SFPResultUpdateRequest(BaseModel):
    sfp_category_id: UUID4
    date: date
    result: float
    notes: str
    goals: str
