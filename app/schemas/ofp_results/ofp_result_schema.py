from datetime import date

from pydantic import UUID4, BaseModel


class OFPResultSchema(BaseModel):
    id: UUID4
    ofp_category_id: UUID4
    date: date
    result: float
    goals: str
    notes: str

    class Config:
        from_attributes = True
