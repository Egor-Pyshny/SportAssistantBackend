from datetime import date

from pydantic import BaseModel, UUID4


class AnthropometricParamsSchema(BaseModel):
    id: UUID4
    date: date
    weight: float
    height: float
    chest_circumference: float

    class Config:
        from_attributes = True