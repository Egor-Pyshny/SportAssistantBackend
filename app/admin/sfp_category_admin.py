from models import SFPCategory
from sqladmin import ModelView


class SFPCategoryAdmin(ModelView, model=SFPCategory):
    column_list = [SFPCategory.id, SFPCategory.name]
