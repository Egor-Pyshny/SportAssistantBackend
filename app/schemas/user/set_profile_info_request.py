import re

from pydantic import UUID4, BaseModel, EmailStr, field_validator


class SetProfileInfoRequest(BaseModel):
    sport_type: str
    qualification: str
    address: str
    phone_number: str
    sex: str
    coach_id: UUID4
