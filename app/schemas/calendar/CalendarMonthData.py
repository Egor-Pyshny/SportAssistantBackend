from datetime import date
from enum import Enum
from typing import Dict, List, Optional

from pydantic import UUID4, BaseModel
from schemas.competition.competition_schema import CompetitionSchema
from schemas.note.note_schema import NoteSchema
from schemas.training_camp.training_camp_schema import TrainingCampSchema


class EventType(str, Enum):
    COMPETITION = "COMPETITION"
    CAMP = "CAMP"
    OFP = "OFP"
    SFP = "SFP"
    MED = "MED"
    COMPREHENSIVE = "COMPREHENSIVE"


class EventData(BaseModel):
    name: str
    id: UUID4
    type: EventType
    dates: List[date]


class CalendarMonthData(BaseModel):
    competition: Optional[CompetitionSchema] = None
    camp: Optional[TrainingCampSchema] = None
    dayNotes: Dict[date, NoteSchema]
    eventDays: Dict[date, List[EventData]]
