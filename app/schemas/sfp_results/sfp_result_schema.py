from datetime import date

from pydantic import UUID4, BaseModel


class SFPResultSchema(BaseModel):
    id: UUID4
    sfp_category_id: UUID4
    date: date
    result: float
    goals: str
    notes: str

    class Config:
        from_attributes = True
