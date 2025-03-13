from datetime import date

from pydantic import BaseModel, UUID4


class AnthropometricParamsUpdateRequest(BaseModel):
    date: date
    weight: float
    height: float
    chest_circumference: float