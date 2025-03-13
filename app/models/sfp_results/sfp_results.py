from uuid import uuid4

from models import Base
from models.general.timestampable_model import TimeStampableModel
from sqlalchemy import UUID, Column, Date, ForeignKey, Text, Float
from sqlalchemy.orm import relationship


class SFPCategory(Base, TimeStampableModel):
    __tablename__ = "tbl_sfp_category"

    id = Column(UUID, primary_key=True, nullable=False, unique=True, default=uuid4)
    name = Column(Text, nullable=False, unique=True)

    results = relationship("SFPResults", back_populates="sfp_category")


class SFPResults(Base, TimeStampableModel):
    __tablename__ = "tbl_sfp_results"

    id = Column(UUID, primary_key=True, nullable=False, unique=True, default=uuid4)
    date = Column(Date)
    result = Column(Float, nullable=False)
    notes = Column(Text, nullable=False)
    goals = Column(Text, nullable=False)

    user_id = Column(UUID, ForeignKey("tbl_user.id"), nullable=False)
    sfp_category_id = Column(UUID, ForeignKey("tbl_sfp_category.id"), nullable=False)
    sfp_category = relationship("SFPCategory", back_populates="results")
