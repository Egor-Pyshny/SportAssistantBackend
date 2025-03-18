from datetime import date

from pydantic import BaseModel


class GraphicPoint(BaseModel):
    value: float
    key: date