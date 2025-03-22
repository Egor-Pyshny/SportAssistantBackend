from pydantic import UUID4, BaseModel, Field


class CompetitionResultUpdateRequest(BaseModel):
    id: UUID4 | None = Field(default=None)
    result: str
    notes: str
