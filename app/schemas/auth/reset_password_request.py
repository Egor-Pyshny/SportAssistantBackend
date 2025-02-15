import re

from pydantic import BaseModel, EmailStr, field_validator


class ResetPasswordRequest(BaseModel):
    email: EmailStr
    password: str
    code: str

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
