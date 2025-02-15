from typing import Optional

from pydantic import BaseModel


class CoachUpdateSchema(BaseModel):
    fio: Optional[str] = None
    phone_number: Optional[str] = None
    institution: Optional[str] = None
