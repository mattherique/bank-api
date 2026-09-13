from dataclasses import dataclass
from app.domain.entities.enums import TransactionType

@dataclass(frozen=True)
class Transaction:
    type: TransactionType
    amount: int
    origin: str | None = None
    destination: str | None = None

    @classmethod
    def deposit(cls, destination: str, amount: int) -> "Transaction":
        return cls(TransactionType.DEPOSIT, amount, destination=destination)

    @classmethod
    def withdraw(cls, origin: str, amount: int) -> "Transaction":
        return cls(TransactionType.WITHDRAW, amount, origin=origin)