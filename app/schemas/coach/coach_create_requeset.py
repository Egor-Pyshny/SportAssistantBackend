from pydantic import BaseModel


class CoachCreateRequest(BaseModel):
    fio: str
    phone_number: str
    institution: str
