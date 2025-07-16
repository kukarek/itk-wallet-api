from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dependencies import get_db
from src.models.schemas.user import Token, UserCreate
from src.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_db),
):
    auth_service = AuthService(session)
    user = await auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    token = auth_service.create_token_for_user(user)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/register", response_model=Token)
async def register(user_create: UserCreate, session: AsyncSession = Depends(get_db)):
    auth_service = AuthService(session)

    # Проверка, что пользователь с таким username ещё не существует
    existing_user = await auth_service.get_user_by_username(user_create.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    user = await auth_service.create_user(user_create)
    token = auth_service.create_token_for_user(user)
    return {"access_token": token, "token_type": "bearer"}
