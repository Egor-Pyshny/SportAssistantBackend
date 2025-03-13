from datetime import date

from pydantic import BaseModel, UUID4


class OFPResultUpdateRequest(BaseModel):
    ofp_category_id: UUID4
    date: date
    result: float
    notes: str
    goals: str
