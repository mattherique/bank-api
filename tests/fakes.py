from app.domain.entities.account import Account
from app.domain.entities.transaction import Transaction
from app.domain.repositories.account import AccountRepository
from app.domain.repositories.transaction import TransactionRepository


class InMemoryAccountRepository(AccountRepository):
    def __init__(self) -> None:
        self._accounts: dict[str, Account] = {}

    def get(self, account_id: str) -> Account | None:
        return self._accounts.get(account_id)

    def get_or_create(self, account_id: str) -> Account:
        if account_id not in self._accounts:
            self._accounts[account_id] = Account(id=account_id, balance=0)
        return self._accounts[account_id]

    def save(self, account: Account) -> None:
        self._accounts[account.id] = account

    def clear(self) -> None:
        self._accounts.clear()


class InMemoryTransactionRepository(TransactionRepository):
    def __init__(self) -> None:
        self._transactions: list[Transaction] = []

    def add(self, transaction: Transaction) -> None:
        self._transactions.append(transaction)

    def list_all(self) -> list[Transaction]:
        return list(self._transactions)

    def clear(self) -> None:
        self._transactions.clear()
