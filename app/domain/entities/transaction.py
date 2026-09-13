from dataclasses import dataclass

from app.domain.entities.enums import TransactionType


@dataclass(frozen=True)
class Transaction:
    type: TransactionType
    amount: int
    origin: str | None = None
    destination: str | None = None

    def __post_init__(self) -> None:
        if self.amount <= 0:
            raise ValueError(f"amount must be positive, got {self.amount}")
        if self.type is TransactionType.DEPOSIT:
            if self.origin is not None or self.destination is None:
                raise ValueError("deposit requires destination and no origin")
        elif self.type is TransactionType.WITHDRAW:
            if self.destination is not None or self.origin is None:
                raise ValueError("withdraw requires origin and no destination")
        elif self.type is TransactionType.TRANSFER:
            if self.origin is None or self.destination is None:
                raise ValueError("transfer requires both origin and destination")

    @classmethod
    def deposit(cls, destination: str, amount: int) -> "Transaction":
        return cls(TransactionType.DEPOSIT, amount, destination=destination)

    @classmethod
    def withdraw(cls, origin: str, amount: int) -> "Transaction":
        return cls(TransactionType.WITHDRAW, amount, origin=origin)

    @classmethod
    def transfer(cls, origin: str, destination: str, amount: int) -> "Transaction":
        return cls(
            TransactionType.TRANSFER, amount, origin=origin, destination=destination
        )
