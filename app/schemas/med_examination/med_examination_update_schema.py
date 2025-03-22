from datetime import date

from pydantic import BaseModel


class MedExaminationUpdateRequest(BaseModel):
    date: date
    institution: str
    methods: str
    recommendations: str
