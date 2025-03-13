from datetime import date

from pydantic import BaseModel, UUID4


class SFPResultCreateRequest(BaseModel):
    sfp_category_id: UUID4
    date: date
    result: float
    goals: str
    notes: str