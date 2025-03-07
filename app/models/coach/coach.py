from uuid import uuid4

from models import Base
from models.general.timestampable_model import TimeStampableModel
from sqlalchemy import UUID, Column, String, Text
from sqlalchemy.orm import relationship


class Coach(Base, TimeStampableModel):
    __tablename__ = "tbl_coach"

    id = Column(UUID, primary_key=True, nullable=False, unique=True, default=uuid4)
    fio = Column(Text, nullable=False, unique=True)
    phone_number = Column(String(30), nullable=False)
    institution = Column(String(50), nullable=False)

    users = relationship("User", back_populates="coach")
