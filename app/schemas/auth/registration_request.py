import re

from pydantic import UUID4, BaseModel, EmailStr, field_validator


class RegistrationRequest(BaseModel):
    name: str
    surname: str
    sport_type: str
    qualification: str
    address: str
    phone_number: str
    sex: str
    coach_id: UUID4
    email: EmailStr
    password: str

    @field_validator("password")
    def validate_password(cls, value):
        pattern = r"^(?=.*?[A-Z,a-z])(?=.*?[0-9])(?=.*?[*@!$#%&()^~{}]).{8,}$"

        if not re.match(pattern, value):
            raise ValueError(
                "Password must contain at least one special character, one digit and one letter"
            )

        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long.")

        return value
