from sqlalchemy.orm import declarative_base

Base = declarative_base()

from models.coach.coach import Coach  # noqa
from models.competition.competition import Competition  # noqa
from models.competition_day.competition_day import CompetitionDay  # noqa
from models.competition_result.competition_result import CompetitionResult  # noqa
from models.user.user import User  # noqa
from models.training_camp.training_camp import TrainingCamp  # noqa
from models.training_camp_day.training_camp_day import TrainingCampDay  # noqa
from models.ofp_results.ofp_results import OFPCategory, OFPResults  # noqa
