from pydantic import BaseModel
from schemas.user.user_schema import UserSchema


class UserWithEmailCodeSchema(BaseModel):
    user: UserSchema
    email_code: str

    def to_redis(self):
        data = self.model_dump(by_alias=True, exclude_unset=True, mode="json")
        flattened = {f"user.{key}": str(value) for key, value in data["user"].items()}
        flattened["email_code"] = data["email_code"]
        return flattened

    @classmethod
    def from_redis(cls, flattened: dict):
        user_data = {k.split("user.")[1]: v for k, v in flattened.items() if k.startswith("user.")}
        email_code = flattened["email_code"]
        combined_data = {
            "user": user_data,
            "email_code": email_code,
        }
        return cls.model_validate(combined_data)
