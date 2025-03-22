from uuid import uuid4

from models import Base
from models.general.timestampable_model import TimeStampableModel
from sqlalchemy import UUID, Column, Date, ForeignKey, Text


class Note(Base, TimeStampableModel):
    __tablename__ = "tbl_note"

    id = Column(UUID, primary_key=True, nullable=False, unique=True, default=uuid4)
    date = Column(Date)
    text = Column(Text, nullable=False, unique=True)

    user_id = Column(UUID, ForeignKey("tbl_user.id"), nullable=False)
