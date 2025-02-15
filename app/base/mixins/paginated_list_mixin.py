from typing import Callable
from uuid import UUID

from crud.general.get_paginated_instances import get_paginated_instances
from crud.general.get_single_instance import get_single_instance
from pydantic import BaseModel
from schemas.general.paginated_response import PaginatedResponse
from sqlalchemy.orm.decl_api import DeclarativeMeta
from sqlalchemy.sql.selectable import Select


class PaginatedListMixin:

    model: DeclarativeMeta
    schema: BaseModel
    not_found_exception_func: Callable

    def _get_query(*args, **kwargs):
        pass

    def _not_found_exception_func(self, instance: DeclarativeMeta | None):
        pass

    async def list(self, cursor_id: UUID | None, limit: int, *args, **kwargs) -> PaginatedResponse:

        query: Select = self._get_query(*args, **kwargs)

        instances: list[DeclarativeMeta] = []
        next_cursor: UUID | None = None
        total_count: int = 0

        instance: DeclarativeMeta | None = None
        if cursor_id:
            instance: DeclarativeMeta = await get_single_instance(self.db, self.model, cursor_id)
            self._not_found_exception_func(instance)

        instances, next_cursor, total_count = await get_paginated_instances(
            self.db, self.model, instance, limit, query
        )

        instances_schema: list[BaseModel] = []
        for instance in instances:
            instances_schema.append(self.schema.model_validate(instance))

        return PaginatedResponse(
            data=instances_schema, next_cursor=next_cursor, total_count=total_count
        )
