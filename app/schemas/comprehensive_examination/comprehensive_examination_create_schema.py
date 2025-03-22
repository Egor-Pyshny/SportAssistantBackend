from datetime import date

from pydantic import BaseModel


class ComprehensiveExaminationCreateRequests(BaseModel):
    date: date
    institution: str
    specialists: str
    methods: str
    recommendations: str
