from django.conf import settings

from app.application.services import BalanceService, ResetService, TransactionService
from app.domain.repositories.account import AccountRepository
from app.domain.repositories.transaction import TransactionRepository

if getattr(settings, "USE_IN_MEMORY_REPOSITORIES", False):
    from app.infrastructure.repositories.in_memory import (
        InMemoryAccountRepository as _AccountRepositoryImpl,
        InMemoryTransactionRepository as _TransactionRepositoryImpl,
    )
else:
    from app.infrastructure.repositories.orm import (
        DjangoAccountRepository as _AccountRepositoryImpl,
        DjangoTransactionRepository as _TransactionRepositoryImpl,
    )

account_repository: AccountRepository = _AccountRepositoryImpl()
transaction_repository: TransactionRepository = _TransactionRepositoryImpl()


def get_transaction_service() -> TransactionService:
    return TransactionService(account_repository, transaction_repository)


def get_balance_service() -> BalanceService:
    return BalanceService(account_repository)


def get_reset_service() -> ResetService:
    return ResetService(account_repository, transaction_repository)
