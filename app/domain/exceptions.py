class DomainError(Exception):
    pass


class AccountNotFound(DomainError):
    def __init__(self, account_id: str) -> None:
        self.account_id = account_id
        super().__init__(f"account {account_id!r} not found")


class InsufficientFunds(DomainError):
    def __init__(self, account_id: str, requested: int, available: int) -> None:
        self.account_id = account_id
        self.requested = requested
        self.available = available
        super().__init__(
            f"account {account_id!r} has {available}, requested {requested}"
        )
