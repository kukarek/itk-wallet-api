from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.db_models import User
from uuid import UUID


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_username(self, username: str) -> User | None:
        result = await self.session.execute(select(User).where(User.username == username))
        return result.scalars().first()

    async def get_by_id(self, user_id: UUID) -> User | None:
        result = await self.session.execute(select(User).where(User.id == user_id))
        return result.scalars().first()

    async def create_user(self, user: User):
        self.session.add(user)
        await self.session.flush() 
        await self.session.commit()
