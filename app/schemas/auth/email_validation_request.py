from pydantic import BaseModel, EmailStr


class EmailValidationRequest(BaseModel):
    email: EmailStr
    code: str
