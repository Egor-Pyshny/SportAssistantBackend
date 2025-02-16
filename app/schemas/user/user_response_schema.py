from datetime import datetime

from pydantic import UUID4, BaseModel, EmailStr

from schemas.coach.coach_schema import CoachSchema


class UserResponseSchema(BaseModel):
    id: UUID4
    name: str
    surname: str
    sport_type: str
    qualification: str
    address: str
    phone_number: str
    sex: str
    coach: CoachSchema
    email: str | EmailStr
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True
