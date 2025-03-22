from datetime import date

from pydantic import UUID4, BaseModel


class MedExaminationSchema(BaseModel):
    id: UUID4
    date: date
    institution: str
    methods: str
    recommendations: str

    class Config:
        from_attributes = True
