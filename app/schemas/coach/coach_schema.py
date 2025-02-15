from typing import List

from pydantic import UUID4, BaseModel, Field
from schemas.user.user_response_schema import UserResponseSchema


class CoachSchema(BaseModel):
    id: UUID4
    fio: str
    phone_number: str
    institution: str

    class Config:
        from_attributes = True
