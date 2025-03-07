from uuid import uuid4

from constants.roles import Roles
from models import Base
from models.general.timestampable_model import TimeStampableModel
from sqlalchemy import UUID, Column, ForeignKey, String, Text
from sqlalchemy.orm import relationship


class User(Base, TimeStampableModel):
    __tablename__ = "tbl_user"

    id = Column(UUID, primary_key=True, nullable=False, unique=True, default=uuid4)
    email = Column(String(50), index=True, nullable=False, unique=True)
    password = Column(Text, nullable=False)
    name = Column(String(30), nullable=False)
    surname = Column(String(30), nullable=False)
    sport_type = Column(String(60), nullable=False)
    qualification = Column(String(60), nullable=False)
    address = Column(String(60), nullable=False)
    phone_number = Column(String(30), nullable=False)
    sex = Column(String(30), nullable=False)
    role: str = Column(String(30), nullable=False, default=Roles.user.value)

    coach_id = Column(UUID, ForeignKey("tbl_coach.id"), nullable=False)
    coach = relationship("Coach", back_populates="users")
