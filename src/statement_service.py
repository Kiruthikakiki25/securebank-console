from sortedcontainers import SortedDict
from src.bank import Bank


class StatementService:
    def __init__(self, bank: Bank):
        self.bank = bank
        self._by_id: SortedDict = SortedDict()
        self._by_balance: SortedDict = SortedDict()

    def register(self, account_id: int):
        """Call after every bank.create() to index the account."""
        acc = self.bank.get(account_id)
        self._by_id[account_id] = acc
        self._by_balance[(acc.balance, account_id)] = acc

    def accounts_sorted_by_id(self) -> list:
        return list(self._by_id.values())

    def accounts_sorted_by_balance(self) -> list:
        return list(self._by_balance.values())

    def accounts_in_id_range(self, lo: int, hi: int) -> list:
        """irange() — no manual loop, O(log n) range query."""
        return [self._by_id[k] for k in self._by_id.irange(lo, hi)]a1 = bank.create("Alice", 500.0)