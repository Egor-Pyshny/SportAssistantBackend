from uuid import uuid4

from models import Base
from models.general.timestampable_model import TimeStampableModel
from sqlalchemy import UUID, Column, Date, ForeignKey, Float


class AnthropometricParams(Base, TimeStampableModel):
    __tablename__ = "tbl_anthropometric_params"

    id = Column(UUID, primary_key=True, nullable=False, unique=True, default=uuid4)
    date = Column(Date)
    weight = Column(Float, nullable=False)
    height = Column(Float, nullable=False)
    chest_circumference = Column(Float, nullable=False)

    user_id = Column(UUID, ForeignKey("tbl_user.id"), nullable=False)
