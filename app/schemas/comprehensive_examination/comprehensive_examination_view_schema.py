from datetime import date

from pydantic import BaseModel, UUID4


class ComprehensiveExaminationViewSchema(BaseModel):
    id: UUID4
    date: date

    class Config:
        from_attributes = True