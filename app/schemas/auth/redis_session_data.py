from pydantic import BaseModel, EmailStr


class RedisSessionData(BaseModel):
    email: EmailStr
