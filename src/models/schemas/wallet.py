from pydantic import BaseModel
from uuid import UUID
from decimal import Decimal


class WalletBase(BaseModel):
    balance: Decimal


class WalletRead(WalletBase):
    id: UUID
    user_id: UUID

    class Config:
        from_attributes = True
