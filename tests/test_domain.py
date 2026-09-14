import unittest

from app.domain.entities.account import Account
from app.domain.entities.enums import TransactionType
from app.domain.entities.transaction import Transaction
from app.domain.exceptions import InsufficientFunds


class AccountTest(unittest.TestCase):
    def test_deposit_adds_to_the_balance(self):
        account = Account("100")
        account.deposit(10)
        account.deposit(10)
        self.assertEqual(account.balance, 20)

    def test_withdraw_subtracts_from_the_balance(self):
        account = Account("100", balance=20)
        account.withdraw(5)
        self.assertEqual(account.balance, 15)

    def test_withdraw_beyond_the_balance_is_rejected(self):
        account = Account("100", balance=10)
        with self.assertRaises(InsufficientFunds):
            account.withdraw(11)
        self.assertEqual(account.balance, 10)

    def test_non_positive_amounts_are_rejected(self):
        for amount in (0, -1):
            with self.subTest(amount=amount):
                account = Account("100", balance=10)
                with self.assertRaises(ValueError):
                    account.deposit(amount)
                with self.assertRaises(ValueError):
                    account.withdraw(amount)
                self.assertEqual(account.balance, 10)


class TransactionTest(unittest.TestCase):
    def test_constructors_fill_the_sides_the_type_requires(self):
        self.assertEqual(
            Transaction.deposit("100", 10),
            Transaction(TransactionType.DEPOSIT, 10, destination="100"),
        )
        self.assertEqual(
            Transaction.withdraw("100", 10),
            Transaction(TransactionType.WITHDRAW, 10, origin="100"),
        )
        self.assertEqual(
            Transaction.transfer("100", "300", 10),
            Transaction(
                TransactionType.TRANSFER, 10, origin="100", destination="300"
            ),
        )

    def test_incoherent_combinations_are_rejected(self):
        cases = [
            (TransactionType.DEPOSIT, {"destination": "100", "origin": "200"}),
            (TransactionType.DEPOSIT, {}),
            (TransactionType.WITHDRAW, {"origin": "100", "destination": "300"}),
            (TransactionType.WITHDRAW, {}),
            (TransactionType.TRANSFER, {"origin": "100"}),
        ]
        for event_type, sides in cases:
            with self.subTest(type=event_type, sides=sides):
                with self.assertRaises(ValueError):
                    Transaction(event_type, 10, **sides)
