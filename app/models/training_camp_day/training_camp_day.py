from uuid import uuid4

from models import Base
from models.general.timestampable_model import TimeStampableModel
from sqlalchemy import UUID, Column, Date, ForeignKey, Text
from sqlalchemy.orm import relationship


class TrainingCampDay(Base, TimeStampableModel):
    __tablename__ = "tbl_training_camp_day"

    id = Column(UUID, primary_key=True, nullable=False, unique=True, default=uuid4)
    date = Column(Date)
    goals = Column(Text, nullable=False, default="")
    notes = Column(Text, nullable=False, default="")

    training_camp_id = Column(UUID, ForeignKey("tbl_training_camp.id"), nullable=False)
    training_camp = relationship("TrainingCamp", back_populates="days")
