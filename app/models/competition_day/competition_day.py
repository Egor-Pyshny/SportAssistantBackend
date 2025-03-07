from uuid import uuid4

from models import Base
from models.general.timestampable_model import TimeStampableModel
from sqlalchemy import UUID, Column, Date, ForeignKey, Text
from sqlalchemy.orm import relationship


class CompetitionDay(Base, TimeStampableModel):
    __tablename__ = "tbl_competition_day"

    id = Column(UUID, primary_key=True, nullable=False, unique=True, default=uuid4)
    date = Column(Date)
    results = Column(Text, nullable=False, default="")
    notes = Column(Text, nullable=False, default="")

    competition_id = Column(UUID, ForeignKey("tbl_competition.id"), nullable=False)
    competition = relationship("Competition", back_populates="days")
