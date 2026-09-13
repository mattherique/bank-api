from app.domain.entities.account import Account
from app.domain.entities.enums import TransactionType
from app.domain.entities.transaction import Transaction
from app.domain.repositories.account import AccountRepository
from app.domain.repositories.transaction import TransactionRepository
from app.infrastructure.models import AccountModel, TransactionModel


class DjangoAccountRepository(AccountRepository):
    def get(self, account_id: str) -> Account | None:
        row = AccountModel.objects.filter(pk=account_id).first()
        return self._to_domain(row) if row is not None else None

    def get_or_create(self, account_id: str) -> Account:
        row, _ = AccountModel.objects.get_or_create(
            pk=account_id, defaults={"balance": 0}
        )
        return self._to_domain(row)

    def save(self, account: Account) -> None:
        AccountModel.objects.update_or_create(
            pk=account.id, defaults={"balance": account.balance}
        )

    def clear(self) -> None:
        AccountModel.objects.all().delete()

    @staticmethod
    def _to_domain(row: AccountModel) -> Account:
        return Account(id=row.id, balance=row.balance)


class DjangoTransactionRepository(TransactionRepository):
    def add(self, transaction: Transaction) -> None:
        TransactionModel.objects.create(
            type=transaction.type.value,
            amount=transaction.amount,
            origin_id=transaction.origin,
            destination_id=transaction.destination,
        )

    def list_all(self) -> list[Transaction]:
        rows = TransactionModel.objects.order_by("timestamp", "id")
        return [self._to_domain(row) for row in rows]

    def clear(self) -> None:
        TransactionModel.objects.all().delete()

    @staticmethod
    def _to_domain(row: TransactionModel) -> Transaction:
        return Transaction(
            type=TransactionType(row.type),
            amount=row.amount,
            origin=row.origin_id,
            destination=row.destination_id,
        )
