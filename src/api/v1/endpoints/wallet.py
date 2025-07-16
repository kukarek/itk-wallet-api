from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dependencies import get_current_user, get_db
from src.models.db_models import User
from src.models.schemas.operation import OperationCreate, OperationRead
from src.models.schemas.wallet import WalletRead
from src.services.wallet_service import WalletService

router = APIRouter(prefix="/wallets", tags=["wallets"])


@router.post("/{wallet_id}/operation", response_model=OperationRead)
async def create_operation(
    wallet_id: UUID,
    operation_data: OperationCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    service = WalletService(session)

    # Проверяем, что кошелек принадлежит текущему пользователю
    wallet = await service.get_wallet(wallet_id, current_user.id)
    if wallet is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Wallet not found")
    if wallet.user_id != current_user.id:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, detail="Not authorized for this wallet"
        )

    try:
        operation = await service.create_operation(wallet_id, operation_data)
    except ValueError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e))

    return operation


@router.get("/{wallet_id}", response_model=WalletRead)
async def get_wallet_balance(
    wallet_id: UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    service = WalletService(session)

    wallet = await service.get_wallet(wallet_id, current_user.id)
    if wallet is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Wallet not found")
    if wallet.user_id != current_user.id:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, detail="Not authorized for this wallet"
        )

    return wallet
