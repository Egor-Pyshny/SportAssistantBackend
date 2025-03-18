from datetime import date

from pydantic import BaseModel, UUID4


class ComprehensiveExaminationUpdateRequest(BaseModel):
    date: date
    institution: str
    specialists: str
    methods: str
    recommendations: str
