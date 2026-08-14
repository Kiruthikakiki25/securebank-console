from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TransactionDTO(BaseModel):
    txn_id: str
    txn_type: str
    amount: float
    to_id: Optional[str] = None
    timestamp: datetime

class AccountDTO(BaseModel):
    account_id: str
    name: str
    balance: float
    is_active: bool
    transactions: list[TransactionDTO] = []

    @classmethod
    def from_account(cls, acc) -> "AccountDTO":
        return cls(
            account_id=acc.account_id,
            name=acc.name,
            balance=acc.balance,
            is_active=acc.is_active,
            transactions=[
                TransactionDTO(
                    txn_id=t.txn_id,
                    txn_type=t.txn_type,
                    amount=t.amount,
                    to_id=t.to_id,
                    timestamp=t.timestamp
                )
                for t in acc.transactions
            ]
        )