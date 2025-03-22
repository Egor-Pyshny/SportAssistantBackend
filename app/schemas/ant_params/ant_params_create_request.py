from datetime import date

from pydantic import BaseModel


class AnthropometricParamsCreateRequest(BaseModel):
    date: date
    weight: float
    height: float
    chest_circumference: float
