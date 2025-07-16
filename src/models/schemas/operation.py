from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field


class OperationType(str, Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"


AmountDecimal = Annotated[
    Decimal,
    Field(gt=0, le=10_000_000, description="Amount must be > 0 and <= 10 million"),
]


class OperationBase(BaseModel):
    operation_type: OperationType
    amount: AmountDecimal


class OperationCreate(OperationBase):
    pass


class OperationRead(OperationBase):
    id: UUID
    wallet_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
