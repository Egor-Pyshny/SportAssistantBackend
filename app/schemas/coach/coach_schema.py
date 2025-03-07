from pydantic import UUID4, BaseModel


class CoachSchema(BaseModel):
    id: UUID4
    fio: str
    phone_number: str
    institution: str

    class Config:
        from_attributes = True
