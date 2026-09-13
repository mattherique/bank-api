from abc import ABC, abstractmethod

from app.domain.entities.transaction import Transaction


class TransactionRepository(ABC):
    @abstractmethod
    def add(self, transaction: Transaction) -> None: ...

    @abstractmethod
    def list_all(self) -> list[Transaction]: ...

    @abstractmethod
    def clear(self) -> None: ...
