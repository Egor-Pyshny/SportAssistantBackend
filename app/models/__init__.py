from sqlalchemy.orm import declarative_base

Base = declarative_base()

from models.coach.coach import Coach  # noqa
from models.user.user import User  # noqa
