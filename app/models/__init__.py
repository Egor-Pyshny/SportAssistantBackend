from sqlalchemy.orm import declarative_base

Base = declarative_base()

from models.coach.coach import Coach  # noqa
from models.competition.competition import Competition  # noqa
from models.competition_day.competition_day import CompetitionDay  # noqa
from models.user.user import User  # noqa
