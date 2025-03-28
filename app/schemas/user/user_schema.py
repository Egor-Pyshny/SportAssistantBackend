from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel, EmailStr


class UserSchema(BaseModel):
    id: UUID4
    name: str
    surname: str
    sport_type: str = ""
    qualification: str = ""
    address: str = ""
    phone_number: str = ""
    sex: str = ""
    coach_id: Optional[UUID4] = None
    email: str | EmailStr
    password: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
