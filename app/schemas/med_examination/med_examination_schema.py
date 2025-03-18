from datetime import date

from pydantic import BaseModel, UUID4


class MedExaminationSchema(BaseModel):
    id: UUID4
    date: date
    institution: str
    methods: str
    recommendations: str

    class Config:
        from_attributes = True