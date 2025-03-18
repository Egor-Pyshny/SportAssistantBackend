from datetime import date

from pydantic import BaseModel, UUID4


class ComprehensiveExaminationSchema(BaseModel):
    id: UUID4
    date: date
    institution: str
    specialists: str
    methods: str
    recommendations: str

    class Config:
        from_attributes = True