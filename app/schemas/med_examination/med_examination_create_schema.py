from datetime import date

from pydantic import BaseModel


class MedExaminationCreateRequest(BaseModel):
    date: date
    institution: str
    methods: str
    recommendations: str
