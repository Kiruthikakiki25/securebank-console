import uuid
from collections import defaultdict
from src.models import Account, Transaction
from src.exceptions import AccountNotFoundError, InsufficientFundsError, AccountClosedError

class Bank:
    def __init__(self):
        self._accounts: dict[str, Account] = {}
        self._transactions: dict[str, Transaction] = {}
        self._name_index: defaultdict[str, list[str]] = defaultdict(list)

    def _get(self, account_id: str) -> Account:
        if account_id not in self._accounts:
            raise AccountNotFoundError(f"Account {account_id} not found.")
        return self._accounts[account_id]

    def create_account(self, owner_name: str, initial_deposit: float = 0.0) -> Account:
        acc = Account(
            account_id=str(uuid.uuid4())[:8],
            owner_name=owner_name,
            balance=initial_deposit
        )
        self._accounts[acc.account_id] = acc
        self._name_index[owner_name.lower()].append(acc.account_id)  # index by name
        return acc

    def deposit(self, account_id: str, amount: float) -> Account:
        acc = self._get(account_id)
        if not acc.is_active:
            raise AccountClosedError("Account is closed.")
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        acc.balance += amount
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
        return acc

    def transfer(self, from_id: str, to_id: str, amount: float) -> Transaction:
    
        self.withdraw(from_id, amount)

        
        try:
            self.deposit(to_id, amount)
        except Exception as e:
            self._get(from_id).balance += amount  # rollback
            raise e
        self._get(from_id).transactions.append(Transaction("transfer_out", amount, to_id))

        
        

    def reverse_last_transaction(self, account_id: str):
        acc = self._get(account_id)
        if not acc.transactions:
            raise ValueError("No transactions to reverse.")
        last = acc.transactions[-1]
    
        if last.txn_type == "deposit":
            acc.balance -= last.amount
        elif last.txn_type == "withdraw":
            acc.balance += last.amount
        elif last.txn_type == "transfer_out":
        
            acc.balance += last.amount
            target = self._get(last.to_id)
            target.balance -= last.amount
    
        acc.transactions.pop()

    def find_by_name(self, name: str) -> list[Account]:
        ids = self._name_index.get(name.lower(), [])
        return [self._accounts[i] for i in ids]