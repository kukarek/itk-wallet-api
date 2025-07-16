from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class WalletBase(BaseModel):
    balance: Decimal


class WalletRead(WalletBase):
    id: UUID
    user_id: UUID

    class Config:
        from_attributes = True
