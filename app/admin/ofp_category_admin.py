from models import OFPCategory
from sqladmin import ModelView


class OFPCategoryAdmin(ModelView, model=OFPCategory):
    column_list = [OFPCategory.id, OFPCategory.name]