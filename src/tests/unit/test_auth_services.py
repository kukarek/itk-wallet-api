from unittest.mock import AsyncMock, MagicMock

import pytest

from src.models.db_models import User
from src.models.schemas.user import UserCreate
from src.services.auth_service import AuthService


@pytest.mark.asyncio
async def test_create_user_and_authenticate():
    session = AsyncMock()
    service = AuthService(session)
    user_data = UserCreate(username="testuser", password="testpass")

    session.add = AsyncMock()
    session.flush = AsyncMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()

    user = await service.create_user(user_data)
    assert user.username == "testuser"
    assert service.verify_password("testpass", user.hashed_password)


@pytest.mark.asyncio
async def test_authenticate_with_wrong_password():
    session = AsyncMock()
    service = AuthService(session)

    user = User(
        username="testuser", hashed_password=service.hash_password("correctpass")
    )

    scalars_mock = MagicMock()
    scalars_mock.first.return_value = user

    execute_result_mock = MagicMock()
    execute_result_mock.scalars.return_value = scalars_mock

    session.execute.return_value = execute_result_mock

    result = await service.authenticate_user("testuser", "wrongpass")
    assert result is None
