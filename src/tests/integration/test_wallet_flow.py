import uuid

import pytest
from jose import jwt
from sqlalchemy.future import select

from src.core.config import get_settings
from src.models.db_models import Wallet

settings = get_settings()


@pytest.mark.asyncio
async def test_wallet_flow(client, db_session):
    resp = await client.post(
        "/api/v1/auth/register",
        json={"username": "walletuser", "password": "walletpass"},
    )
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    payload = jwt.decode(
        token, settings.jwt.SECRET_KEY, algorithms=[settings.jwt.ALGORITHM]
    )
    user_id = payload.get("sub")

    result = await db_session.execute(
        select(Wallet).where(Wallet.user_id == uuid.UUID(user_id))
    )
    wallet = result.scalars().first()
    wallet_id = wallet.id

    response = await client.post(
        f"/api/v1/wallets/{wallet_id}/operation",
        json={"operation_type": "DEPOSIT", "amount": 1000},
        headers=headers,
    )
    assert response.status_code == 200

    response = await client.get(
        f"/api/v1/wallets/{uuid.UUID(wallet_id)}", headers=headers
    )
    assert response.status_code == 200
    assert "balance" in response.json()
