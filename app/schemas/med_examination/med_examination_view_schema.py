from datetime import date

from pydantic import BaseModel, UUID4


class MedExaminationViewSchema(BaseModel):
    id: UUID4
    date: date

    class Config:
        from_attributes = True