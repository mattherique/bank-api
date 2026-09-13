class TransactionService:
    def __init__(self, account_repository, transaction_repository):
        self.account_repository = account_repository
        self.transaction_repository = transaction_repository

    def deposit(self, account_id, amount):
        account = self.account_repository.get_account(account_id)
        if account is None:
            raise ValueError("Account not found")
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        account.deposit(amount)
        self.account_repository.update_account(account)

    def withdraw(self, account_id, amount):
        account = self.account_repository.get_account(account_id)
        if account is None:
            raise ValueError("Account not found")
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > account.get_balance():
            raise ValueError("Insufficient funds")
        account.withdraw(amount)
        self.account_repository.update_account(account)

class BalanceService:
    def __init__(self, account_repository):
        self.account_repository = account_repository

    def get_balance(self, account_id):
        account = self.account_repository.get_account(account_id)
        if account is None:
            raise ValueError("Account not found")
        return account.get_balance()

class ResetService:
    def __init__(self, account_repository, transaction_repository):
        self.account_repository = account_repository
        self.transaction_repository = transaction_repository

    def reset(self):
        self.account_repository.clear()
        self.transaction_repository.clear()