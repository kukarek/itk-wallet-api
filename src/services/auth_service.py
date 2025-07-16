from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import get_settings
from src.models.db_models import User, Wallet
from src.models.schemas.user import UserCreate
from src.repository.user import UserRepository
from src.repository.wallet import WalletRepository

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository(session)
        self.wallet_repo = WalletRepository(session)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def create_token_for_user(self, user: User) -> str:
        payload = {"sub": str(user.id)}
        token = jwt.encode(
            payload, settings.jwt.SECRET_KEY, algorithm=settings.jwt.ALGORITHM
        )
        return token

    async def get_user_by_username(self, username: str) -> User | None:
        return await self.user_repo.get_by_username(username)

    async def authenticate_user(self, username: str, password: str) -> User | None:
        user = await self.get_user_by_username(username)
        if not user:
            return None
        if not self.verify_password(password, user.hashed_password):
            return None
        return user

    async def create_user(self, user_create: UserCreate) -> User:
        hashed_password = self.hash_password(user_create.password)

        new_user = User(username=user_create.username, hashed_password=hashed_password)

        await self.user_repo.create_user(new_user)
        # Создаем кошелек при создании пользователя
        await self.wallet_repo.create_wallet(new_user.id)

        return new_user
