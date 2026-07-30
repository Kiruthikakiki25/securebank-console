import uuid
from src.models import Account
from src.exceptions import (
    AccountNotFoundError,
    InsufficientFundsError,
    AccountClosedError,
    DuplicateAccountError,
)

class Bank:
    def __init__(self):
        self._accounts: dict[str, Account] = {}

    def _get(self, account_id: str) -> Account:
        """Fetch account or raise. Used internally."""
        if account_id not in self._accounts:
            raise AccountNotFoundError(f"Account {account_id} not found.")
        return self._accounts[account_id]

    def create_account(self, owner_name: str, initial_deposit: float = 0.0) -> Account:
        account_id = str(uuid.uuid4())[:8]          # short 8-char ID
        if initial_deposit < 0:
            raise ValueError("Initial deposit cannot be negative.")
        acc = Account(account_id=account_id, owner_name=owner_name, balance=initial_deposit)
        self._accounts[account_id] = acc
        return acc

    def deposit(self, account_id: str, amount: float) -> Account:
        acc = self._get(account_id)
        if not acc.is_active:
            raise AccountClosedError(f"Account {account_id} is closed.")
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        acc.balance += amount
        return acc

    def withdraw(self, account_id: str, amount: float) -> Account:
        acc = self._get(account_id)
        if not acc.is_active:
            raise AccountClosedError(f"Account {account_id} is closed.")
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if acc.balance < amount:
            raise InsufficientFundsError(
                f"Balance {acc.balance:.2f} < requested {amount:.2f}."
            )
        acc.balance -= amount
        return acc

    def get_balance(self, account_id: str) -> float:
        acc = self._get(account_id)
        if not acc.is_active:
            raise AccountClosedError(f"Account {account_id} is closed.")
        return acc.balance

    def close_account(self, account_id: str) -> Account:
        acc = self._get(account_id)
        if not acc.is_active:
            raise AccountClosedError(f"Account {account_id} is already closed.")
        acc.is_active = False
        return acc

    def list_accounts(self) -> list[Account]:
        return list(self._accounts.values())