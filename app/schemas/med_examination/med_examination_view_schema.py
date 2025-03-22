from datetime import date

from pydantic import UUID4, BaseModel


class MedExaminationViewSchema(BaseModel):
    id: UUID4
    date: date

    class Config:
        from_attributes = True
