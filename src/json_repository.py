import json
from pathlib import Path
from typing import Optional
from dataclasses import asdict
from datetime import datetime
from src.models import Account, Transaction
from src.repository import AccountRepository

DATA_FILE = Path("data/accounts.json")

def _serialize(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Cannot serialize {type(obj)}")

def _account_from_dict(d: dict) -> Account:
    txns = [
        Transaction(
            txn_id=t["txn_id"],
            txn_type=t["txn_type"],
            amount=t["amount"],
            to_id=t.get("to_id"),
            timestamp=datetime.fromisoformat(t["timestamp"])
        )
        for t in d.get("transactions", [])
    ]
    return Account(
        account_id=d["account_id"],
        name=d["name"],
        balance=d["balance"],
        is_active=d["is_active"],
        transactions=txns
    )

class JsonAccountRepository(AccountRepository):

    def __init__(self):
        DATA_FILE.parent.mkdir(exist_ok=True)
        if not DATA_FILE.exists():
            DATA_FILE.write_text("[]")

    def _load(self) -> dict[str, Account]:
        raw = json.loads(DATA_FILE.read_text())
        return {d["account_id"]: _account_from_dict(d) for d in raw}

    def _persist(self, store: dict[str, Account]) -> None:
        raw = [asdict(acc) for acc in store.values()]
        DATA_FILE.write_text(json.dumps(raw, default=_serialize, indent=2))

    def save(self, account: Account) -> None:
        store = self._load()
        store[account.account_id] = account
        self._persist(store)

    def get(self, account_id: str) -> Optional[Account]:
        store = self._load()
        return store.get(account_id)

    def list_all(self) -> list[Account]:
        return list(self._load().values())

    def delete(self, account_id: str) -> None:
        store = self._load()
        store.pop(account_id, None)
        self._persist(store)