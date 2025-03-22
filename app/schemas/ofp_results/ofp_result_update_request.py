from datetime import date

from pydantic import UUID4, BaseModel


class OFPResultUpdateRequest(BaseModel):
    ofp_category_id: UUID4
    date: date
    result: float
    notes: str
    goals: str
