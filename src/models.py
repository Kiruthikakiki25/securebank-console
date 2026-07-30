from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Account:
    account_id: str
    owner_name: str
    balance: float = 0.0
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)