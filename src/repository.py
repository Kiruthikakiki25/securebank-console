from abc import ABC, abstractmethod
from typing import Optional
from src.models import Account

class AccountRepository(ABC):

    @abstractmethod
    def save(self, account: Account) -> None:
        pass

    @abstractmethod
    def get(self, account_id: str) -> Optional[Account]:
        pass

    @abstractmethod
    def list_all(self) -> list[Account]:
        pass

    @abstractmethod
    def delete(self, account_id: str) -> None:
        pass


class InMemoryAccountRepository(AccountRepository):

    def __init__(self):
        self._store: dict[str, Account] = {}

    def save(self, account: Account) -> None:
        self._store[account.account_id] = account

    def get(self, account_id: str) -> Optional[Account]:
        return self._store.get(account_id)

    def list_all(self) -> list[Account]:
        return list(self._store.values())

    def delete(self, account_id: str) -> None:
        self._store.pop(account_id, None)