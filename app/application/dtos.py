from dataclasses import dataclass


@dataclass(frozen=True)
class DepositDTO:
    destination: str
    amount: int


@dataclass(frozen=True)
class WithdrawDTO:
    origin: str
    amount: int


@dataclass(frozen=True)
class TransferDTO:
    origin: str
    destination: str
    amount: int
