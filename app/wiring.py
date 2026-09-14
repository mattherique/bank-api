from app.application.services import BalanceService, ResetService, TransactionService
from app.domain.repositories.account import AccountRepository
from app.domain.repositories.transaction import TransactionRepository
from app.infrastructure.repositories.orm import (
    DjangoAccountRepository,
    DjangoTransactionRepository,
)

account_repository: AccountRepository = DjangoAccountRepository()
transaction_repository: TransactionRepository = DjangoTransactionRepository()


def get_transaction_service() -> TransactionService:
    return TransactionService(account_repository, transaction_repository)


def get_balance_service() -> BalanceService:
    return BalanceService(account_repository)


def get_reset_service() -> ResetService:
    return ResetService(account_repository, transaction_repository)