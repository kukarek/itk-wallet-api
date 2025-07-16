from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from decimal import Decimal
from fastapi import HTTPException, status

from src.models.db_models import Wallet, OperationType
from src.models.schemas.operation import OperationCreate, OperationRead
from src.repository.wallet import WalletRepository


class WalletService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = WalletRepository(session)

    async def get_wallet(self, wallet_id: UUID, user_id: UUID) -> Wallet:
        wallet = await self.repo.get_wallet(wallet_id)
        if not wallet:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Wallet not found")
        if wallet.user_id != user_id:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN, detail="Operation not permitted"
            )
        return wallet

    async def create_operation(self, wallet_id: UUID, op_create: OperationCreate) -> OperationRead:
        wallet = await self.repo.get_wallet(wallet_id)
        if not wallet:
            raise ValueError("Wallet not found")

        amount: Decimal = op_create.amount
        if amount <= 0:
            raise ValueError("Amount must be positive")

        if op_create.operation_type == OperationType.WITHDRAW and wallet.balance < amount:
            raise ValueError("Insufficient funds")

        await self.repo.update_balance(wallet, amount, op_create.operation_type)
        operation = await self.repo.create_operation(wallet_id, op_create.operation_type, amount)

        await self.repo.commit()
        await self.repo.refresh(operation)

        return OperationRead.model_validate(operation)
