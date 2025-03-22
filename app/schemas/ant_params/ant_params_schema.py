from datetime import date

from pydantic import UUID4, BaseModel


class AnthropometricParamsSchema(BaseModel):
    id: UUID4
    date: date
    weight: float
    height: float
    chest_circumference: float

    class Config:
        from_attributes = True
