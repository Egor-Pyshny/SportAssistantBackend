from enum import Enum


class CompetitionStatus(str, Enum):
    past = "past"
    current = "current"
    next = "next"
