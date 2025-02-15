from models import User
from pydantic import EmailStr
from sqlalchemy import UUID, select, update
from sqlalchemy.ext.asyncio import AsyncSession


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
        query = select(User).where(User.email == email)
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
