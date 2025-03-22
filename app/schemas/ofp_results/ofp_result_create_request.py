from datetime import date

from pydantic import UUID4, BaseModel


class OFPResultCreateRequest(BaseModel):
    ofp_category_id: UUID4
    date: date
    result: float
    goals: str
    notes: str
