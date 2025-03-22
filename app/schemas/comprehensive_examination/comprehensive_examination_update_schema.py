from datetime import date

from pydantic import BaseModel


class ComprehensiveExaminationUpdateRequest(BaseModel):
    date: date
    institution: str
    specialists: str
    methods: str
    recommendations: str
