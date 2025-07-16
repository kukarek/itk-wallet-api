from decimal import Decimal
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.db_models import Operation, OperationType, Wallet


class WalletRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_wallet(
        self, user_id: UUID, initial_balance: Decimal = Decimal("0")
    ) -> Wallet:
        wallet = Wallet(user_id=user_id, balance=initial_balance)
        self.session.add(wallet)
        await self.session.flush()
        await self.session.commit()
        return wallet

    async def get_wallet(self, wallet_id: UUID) -> Wallet | None:
        result = await self.session.execute(
            select(Wallet).where(Wallet.id == wallet_id)
        )
        return result.scalars().first()

    async def update_balance(
        self, wallet: Wallet, amount: Decimal, operation_type: OperationType
    ) -> None:
        if operation_type == OperationType.WITHDRAW:
            wallet.balance -= amount
        else:
            wallet.balance += amount
        self.session.add(wallet)

    async def create_operation(
        self, wallet_id: UUID, operation_type: OperationType, amount: Decimal
    ) -> Operation:
        operation = Operation(
            wallet_id=wallet_id,
            operation_type=operation_type,
            amount=amount,
        )
        self.session.add(operation)
        return operation

    async def commit(self):
        await self.session.commit()

    async def refresh(self, instance):
        await self.session.refresh(instance)
