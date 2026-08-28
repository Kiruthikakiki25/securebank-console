from src.repository import AccountRepository
from src.models import Account, Transaction
from src.exceptions import AccountNotFoundError, InsufficientFundsError, AccountClosedError
import uuid

class AccountService:
    def __init__(self, repo: AccountRepository):
        self.repo = repo

    def _get(self, account_id: str) -> Account:
        acc = self.repo.get(account_id)
        if acc is None:
            raise AccountNotFoundError(f"Account {account_id} not found.")
        return acc

    def create_account(self, name: str, initial_deposit: float = 0.0) -> Account:
        acc = Account(
            account_id=str(uuid.uuid4())[:8],
            name=name,
            balance=initial_deposit
        )
        self.repo.save(acc)
        return acc

    def deposit(self, account_id: str, amount: float) -> Account:
        acc = self._get(account_id)
        if not acc.is_active:
            raise AccountClosedError("Account is closed.")
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        acc.balance += amount
        txn = Transaction(txn_id=str(uuid.uuid4())[:8], txn_type="deposit", amount=amount)
        acc.transactions.append(txn)
        self.repo.save(acc)
        return acc

    def withdraw(self, account_id: str, amount: float) -> Account:
        acc = self._get(account_id)
        if not acc.is_active:
            raise AccountClosedError("Account is closed.")
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        if acc.balance < amount:
            raise InsufficientFundsError("Insufficient funds.")
        acc.balance -= amount
        txn = Transaction(txn_id=str(uuid.uuid4())[:8], txn_type="withdraw", amount=amount)
        acc.transactions.append(txn)
        self.repo.save(acc)
        return acc

    def transfer(self, from_id: str, to_id: str, amount: float) -> Account:
        self.withdraw(from_id, amount)
        try:
            self.deposit(to_id, amount)
        except Exception as e:
            self._get(from_id).balance += amount
            self.repo.save(self._get(from_id))
            raise e
        return self._get(from_id)

    def close_account(self, account_id: str) -> Account:
        acc = self._get(account_id)
        acc.is_active = False
        self.repo.save(acc)
        return acc

    def list_accounts(self) -> list[Account]:
        return self.repo.list_all()