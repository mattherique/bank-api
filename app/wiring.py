from typing import Callable

from django.conf import settings

from app.application.services import BalanceService, ResetService, TransactionService
from app.domain.repositories.account import AccountRepository
from app.domain.repositories.transaction import TransactionRepository
from app.domain.unit_of_work import UnitOfWork

if getattr(settings, "USE_IN_MEMORY_REPOSITORIES", False):
    from app.infrastructure.repositories.in_memory import (
        InMemoryAccountRepository as _AccountRepositoryImpl,
        InMemoryTransactionRepository as _TransactionRepositoryImpl,
    )
    from app.infrastructure.unit_of_work.in_memory import (
        NullUnitOfWork as _UnitOfWorkImpl,
    )
else:
    from app.infrastructure.repositories.orm import (
        DjangoAccountRepository as _AccountRepositoryImpl,
        DjangoTransactionRepository as _TransactionRepositoryImpl,
    )
    from app.infrastructure.unit_of_work.orm import (
        DjangoUnitOfWork as _UnitOfWorkImpl,
    )

account_repository: AccountRepository = _AccountRepositoryImpl()
transaction_repository: TransactionRepository = _TransactionRepositoryImpl()
unit_of_work: Callable[[], UnitOfWork] = _UnitOfWorkImpl


def get_transaction_service() -> TransactionService:
    return TransactionService(account_repository, transaction_repository, unit_of_work)


def get_balance_service() -> BalanceService:
    return BalanceService(account_repository)


def get_reset_service() -> ResetService:
    return ResetService(account_repository, transaction_repository, unit_of_work)
