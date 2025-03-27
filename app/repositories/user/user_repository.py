from models import User
from pydantic import EmailStr
from sqlalchemy import UUID, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import subqueryload

from schemas.user.set_profile_info_request import SetProfileInfoRequest


class UserRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    # @async_transaction
    async def is_unique_email(self, email: str | EmailStr) -> bool:
        query = select(User).where(User.email == email)
        result = await self.db.execute(query)
        existing_user = result.scalars().first()
        return existing_user is not None

    # @async_transaction
    async def is_unique_name(self, user_name: str) -> bool:
        query = select(User).where(User.name == user_name)
        result = await self.db.execute(query)
        existing_user = result.scalars().first()
        return existing_user is not None

    # @async_transaction
    async def create_user(self, new_user: User) -> User:
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user

    # @async_transaction
    async def get_user_by_email(self, email: str | EmailStr) -> User | None:
        query = select(User).options(subqueryload(User.coach)).where(User.email == email)
        result = await self.db.execute(query)
        return result.scalars().first()

    # @async_transaction
    async def get_user_by_id(self, user_id: UUID) -> User | None:
        query = select(User).where(User.id == user_id)
        result = await self.db.execute(query)
        return result.scalars().first()

    # @async_transaction
    async def change_user_password(self, user_email: str | EmailStr, new_password: str) -> bool:
        query = update(User).where(User.email == user_email).values(password=new_password)
        result = await self.db.execute(query)
        await self.db.commit()
        return result.rowcount > 0

    async def fill_data(self, user_id: UUID, data: SetProfileInfoRequest):
        query = update(User).where(User.id == user_id).values(
            sport_type=data.sport_type,
            qualification=data.qualification,
            address=data.qualification,
            phone_number=data.phone_number,
            sex=data.sex,
            coach_id=data.coach_id,
            is_info_filled=True,
        )
        result = await self.db.execute(query)
        await self.db.commit()
