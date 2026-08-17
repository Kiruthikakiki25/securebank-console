from dataclasses import dataclass, field
from datetime import datetime
import uuid

@dataclass
class Account:
    account_id: int
    name: str
    balance: float
    is_active: bool = True
    transactions: list = field(default_factory=list)

@dataclass
class Transaction:
    txn_id: str
    txn_type: str       
    amount: float
    to_id: int | None = None
    timestamp: datetime = field(default_factory=datetime.now)