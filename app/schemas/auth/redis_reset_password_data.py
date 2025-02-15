from pydantic import BaseModel


class RedisResetPasswordData(BaseModel):
    code: str
