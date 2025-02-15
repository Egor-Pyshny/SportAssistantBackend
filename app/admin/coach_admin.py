from models import Coach
from sqladmin import ModelView


class CoachAdmin(ModelView, model=Coach):
    column_list = [Coach.id, Coach.fio]
