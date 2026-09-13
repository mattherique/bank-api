from typing import Callable

from app.application.dtos import DepositDTO, TransferDTO, WithdrawDTO
from app.domain.entities.account import Account
from app.domain.entities.transaction import Transaction
from app.domain.exceptions import AccountNotFound
from app.domain.repositories.account import AccountRepository
from app.domain.repositories.transaction import TransactionRepository
from app.domain.unit_of_work import UnitOfWork


class TransactionService:
    def __init__(
        self,
        account_repository: AccountRepository,
        transaction_repository: TransactionRepository,
        unit_of_work: Callable[[], UnitOfWork],
    ) -> None:
        self.account_repository = account_repository
        self.transaction_repository = transaction_repository
        self.unit_of_work = unit_of_work

    def deposit(self, dto: DepositDTO) -> Account:
        with self.unit_of_work():
            account = self.account_repository.get_or_create(dto.destination)
            account.deposit(dto.amount)
            self.account_repository.save(account)
            self.transaction_repository.add(
                Transaction.deposit(dto.destination, dto.amount)
            )
        return account

    def withdraw(self, dto: WithdrawDTO) -> Account:
        with self.unit_of_work():
            account = self._require(dto.origin)
            account.withdraw(dto.amount)
            self.account_repository.save(account)
            self.transaction_repository.add(
                Transaction.withdraw(dto.origin, dto.amount)
            )
        return account

    def transfer(self, dto: TransferDTO) -> tuple[Account, Account]:
        with self.unit_of_work():
            origin = self._require(dto.origin)
            origin.withdraw(dto.amount)

            destination = self.account_repository.get_or_create(dto.destination)
            destination.deposit(dto.amount)

            self.account_repository.save(origin)
            self.account_repository.save(destination)
            self.transaction_repository.add(
                Transaction.transfer(dto.origin, dto.destination, dto.amount)
            )
        return origin, destination

    def _require(self, account_id: str) -> Account:
        account = self.account_repository.get(account_id)
        if account is None:
            raise AccountNotFound(account_id)
        return account


class BalanceService:
    def __init__(self, account_repository: AccountRepository) -> None:
        self.account_repository = account_repository

    def get_balance(self, account_id: str) -> int:
        account = self.account_repository.get(account_id)
        if account is None:
            raise AccountNotFound(account_id)
        return account.balance


class ResetService:
    def __init__(
        self,
        account_repository: AccountRepository,
        transaction_repository: TransactionRepository,
        unit_of_work: Callable[[], UnitOfWork],
    ) -> None:
        self.account_repository = account_repository
        self.transaction_repository = transaction_repository
        self.unit_of_work = unit_of_work

    def reset(self) -> None:
        with self.unit_of_work():
            self.account_repository.clear()
            self.transaction_repository.clear()
