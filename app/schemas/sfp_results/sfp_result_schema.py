from datetime import date

from pydantic import BaseModel, UUID4


class SFPResultSchema(BaseModel):
    id: UUID4
    sfp_category_id: UUID4
    date: date
    result: float
    goals: str
    notes: str

    class Config:
        from_attributes = True
