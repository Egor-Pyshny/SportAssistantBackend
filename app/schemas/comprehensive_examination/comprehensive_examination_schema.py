from datetime import date

from pydantic import UUID4, BaseModel


class ComprehensiveExaminationSchema(BaseModel):
    id: UUID4
    date: date
    institution: str
    specialists: str
    methods: str
    recommendations: str

    class Config:
        from_attributes = True
