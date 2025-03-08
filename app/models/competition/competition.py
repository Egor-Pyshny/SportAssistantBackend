from uuid import uuid4

from models import Base
from models.general.timestampable_model import TimeStampableModel
from sqlalchemy import UUID, Column, Date, ForeignKey, Text
from sqlalchemy.orm import relationship


class Competition(Base, TimeStampableModel):
    __tablename__ = "tbl_competition"

    id = Column(UUID, primary_key=True, nullable=False, unique=True, default=uuid4)
    start_date = Column(Date)
    end_date = Column(Date)
    location = Column(Text, nullable=False)
    name = Column(Text, nullable=False)
    notes = Column(Text, nullable=False)

    user_id = Column(UUID, ForeignKey("tbl_user.id"), nullable=False)
    days = relationship(
        "CompetitionDay", back_populates="competition", cascade="all, delete-orphan"
    )
