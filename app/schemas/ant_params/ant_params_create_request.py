from datetime import date

from pydantic import BaseModel, UUID4


class AnthropometricParamsCreateRequest(BaseModel):
    date: date
    weight: float
    height: float
    chest_circumference: float