class Account:
    def __init__(self, id: str, balance: int):
        self.id = id
        self.balance = balance

    def deposit(self, amount):
        raise NotImplementedError("Deposit method not implemented yet.")

    def withdraw(self, amount):
        raise NotImplementedError("Withdraw method not implemented yet.")

    def get_balance(self):
        return self.balance