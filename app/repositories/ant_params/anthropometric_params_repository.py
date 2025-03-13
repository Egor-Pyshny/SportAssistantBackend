from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import AnthropometricParams
from schemas.ant_params.ant_params_update_request import AnthropometricParamsUpdateRequest


class AnthropometricParamsRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, params: AnthropometricParams) -> AnthropometricParams:
        self.db.add(params)
        await self.db.commit()
        await self.db.refresh(params)
        return params

    async def get_all(self, id: UUID4):
        query = select(AnthropometricParams).where(AnthropometricParams.user_id == id)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def delete(self, params_id: UUID4):
        query = select(AnthropometricParams).where(AnthropometricParams.id == params_id)
        result = await self.db.execute(query)
        params: AnthropometricParams | None = result.scalar_one_or_none()
        if params:
            await self.db.delete(params)
            await self.db.commit()
            return True
        return False

    async def update(self, body: AnthropometricParamsUpdateRequest, params_id: UUID4):
        query = select(AnthropometricParams).where(AnthropometricParams.id == params_id)
        result = await self.db.execute(query)
        params: AnthropometricParams | None = result.scalar_one_or_none()
        if params:
            params.date = body.date
            params.height = body.height
            params.weight = body.weight
            params.chest_circumference = body.chest_circumference
            self.db.add(params)
            await self.db.commit()
            await self.db.refresh(params)
            return params
        return None

    async def get(self, params_id):
        query = select(AnthropometricParams).where(AnthropometricParams.id == params_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
