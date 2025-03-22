from datetime import date

from pydantic import UUID4, BaseModel


class SFPResultViewSchema(BaseModel):
    id: UUID4
    date: date

    class Config:
        from_attributes = True
