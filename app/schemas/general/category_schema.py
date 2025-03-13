from pydantic import BaseModel, UUID4


class CategorySchema(BaseModel):
    id: UUID4
    name: str

    class Config:
        from_attributes = True