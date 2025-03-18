from datetime import date

from pydantic import BaseModel, UUID4


class MedExaminationCreateRequest(BaseModel):
    date: date
    institution: str
    methods: str
    recommendations: str
