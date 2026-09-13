from enum import Enum

class TransactionType(str, Enum):
    DEPOSIT  = "deposit"
    WITHDRAW = "withdraw"
    TRANSFER = "transfer"