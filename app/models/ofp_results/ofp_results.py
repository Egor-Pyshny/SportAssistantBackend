from uuid import uuid4

from models import Base
from models.general.timestampable_model import TimeStampableModel
from sqlalchemy import UUID, Column, Date, Float, ForeignKey, Text
from sqlalchemy.orm import relationship


class OFPCategory(Base, TimeStampableModel):
    __tablename__ = "tbl_ofp_category"

    id = Column(UUID, primary_key=True, nullable=False, unique=True, default=uuid4)
    name = Column(Text, nullable=False, unique=True)

    results = relationship("OFPResults", back_populates="ofp_category")


class OFPResults(Base, TimeStampableModel):
    __tablename__ = "tbl_ofp_results"

    id = Column(UUID, primary_key=True, nullable=False, unique=True, default=uuid4)
    date = Column(Date)
    result = Column(Float, nullable=False)
    notes = Column(Text, nullable=False)
    goals = Column(Text, nullable=False)

    user_id = Column(UUID, ForeignKey("tbl_user.id"), nullable=False)
    ofp_category_id = Column(UUID, ForeignKey("tbl_ofp_category.id"), nullable=False)
    ofp_category = relationship("OFPCategory", back_populates="results")
