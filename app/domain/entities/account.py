from app.domain.exceptions import InsufficientFunds


class Account:
    def __init__(self, id: str, balance: int = 0) -> None:
        self.id = id
        self.balance = balance

    def deposit(self, amount: int) -> None:
        self._require_positive(amount)
        self.balance += amount

    def withdraw(self, amount: int) -> None:
        self._require_positive(amount)
        if amount > self.balance:
            raise InsufficientFunds(self.id, requested=amount, available=self.balance)
        self.balance -= amount

    @staticmethod
    def _require_positive(amount: int) -> None:
        if amount <= 0:
            raise ValueError(f"amount must be positive, got {amount}")

    def __repr__(self) -> str:
        return f"Account(id={self.id!r}, balance={self.balance})"
