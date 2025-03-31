import re

from fastapi import HTTPException
from pydantic import UUID4, BaseModel, EmailStr, field_validator
from starlette import status


class RegistrationRequest(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: str
    device_id: UUID4

    @field_validator("password")
    def validate_password(cls, value):
        pattern = r"^(?=.*?[A-Z,a-z])(?=.*?[0-9])(?=.*?[*@!$#%&()^~{}]).{8,}$"

        if not re.match(pattern, value):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": "Password must contain at least one special character, one digit and one letter"
                },
            )

        if len(value) < 8:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"message": "Password must be at least 8 characters long."},
            )

        return value
