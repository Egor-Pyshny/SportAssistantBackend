from pydantic import UUID4, BaseModel, EmailStr


class RedisSessionData(BaseModel):
    email: EmailStr
    id: UUID4
