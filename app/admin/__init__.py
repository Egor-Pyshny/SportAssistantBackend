from models import Competition
from sqladmin import ModelView


class CompetitionAdmin(ModelView, model=Competition):
    column_list = [Competition.id, Competition.user_id]
