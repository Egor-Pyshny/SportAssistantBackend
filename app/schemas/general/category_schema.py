from pydantic import UUID4, BaseModel


class CategorySchema(BaseModel):
    id: UUID4
    name: str

    class Config:
        from_attributes = True
