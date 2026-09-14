from app.domain.unit_of_work import UnitOfWork


class NullUnitOfWork(UnitOfWork):
    def __enter__(self) -> "NullUnitOfWork":
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        return False
