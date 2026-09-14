from django.db import transaction as db_transaction

from app.domain.unit_of_work import UnitOfWork


class DjangoUnitOfWork(UnitOfWork):
    def __enter__(self) -> "DjangoUnitOfWork":
        self._atomic = db_transaction.atomic()
        self._atomic.__enter__()
        return self

    def __exit__(self, exc_type, exc, tb) -> bool | None:
        return self._atomic.__exit__(exc_type, exc, tb)
