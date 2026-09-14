import unittest

from app.application.dtos import DepositDTO, TransferDTO, WithdrawDTO
from app.application.services import BalanceService, ResetService, TransactionService
from app.domain.exceptions import AccountNotFound
from app.infrastructure.repositories.in_memory import (
    InMemoryAccountRepository,
    InMemoryTransactionRepository,
)
from app.infrastructure.unit_of_work.in_memory import NullUnitOfWork


class ServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.accounts = InMemoryAccountRepository()
        self.transactions = InMemoryTransactionRepository()
        self.events = TransactionService(
            self.accounts, self.transactions, NullUnitOfWork
        )
        self.balances = BalanceService(self.accounts)
        self.resets = ResetService(
            self.accounts, self.transactions, NullUnitOfWork
        )


class DepositTest(ServiceTestCase):
    def test_creates_the_account_when_it_does_not_exist(self):
        account = self.events.deposit(DepositDTO("100", 10))
        self.assertEqual((account.id, account.balance), ("100", 10))

    def test_adds_to_an_existing_account(self):
        self.events.deposit(DepositDTO("100", 10))
        account = self.events.deposit(DepositDTO("100", 10))
        self.assertEqual(account.balance, 20)


class WithdrawTest(ServiceTestCase):
    def test_debits_the_account(self):
        self.events.deposit(DepositDTO("100", 20))
        account = self.events.withdraw(WithdrawDTO("100", 5))
        self.assertEqual(account.balance, 15)

    def test_unknown_account_is_rejected(self):
        with self.assertRaises(AccountNotFound):
            self.events.withdraw(WithdrawDTO("200", 10))


class TransferTest(ServiceTestCase):
    def test_moves_the_amount_and_creates_the_destination(self):
        self.events.deposit(DepositDTO("100", 15))
        origin, destination = self.events.transfer(TransferDTO("100", "300", 15))
        self.assertEqual((origin.balance, destination.balance), (0, 15))
        self.assertEqual(self.balances.get_balance("300"), 15)

    def test_unknown_origin_is_rejected_without_creating_the_destination(self):
        with self.assertRaises(AccountNotFound):
            self.events.transfer(TransferDTO("200", "300", 15))
        self.assertIsNone(self.accounts.get("300"))


class BalanceTest(ServiceTestCase):
    def test_a_drained_account_still_exists(self):
        self.events.deposit(DepositDTO("100", 10))
        self.events.withdraw(WithdrawDTO("100", 10))
        self.assertEqual(self.balances.get_balance("100"), 0)

    def test_unknown_account_is_rejected(self):
        with self.assertRaises(AccountNotFound):
            self.balances.get_balance("1234")


class LedgerTest(ServiceTestCase):
    def test_accepted_events_are_recorded_and_rejected_ones_are_not(self):
        self.events.deposit(DepositDTO("100", 20))
        self.events.withdraw(WithdrawDTO("100", 5))
        self.events.transfer(TransferDTO("100", "300", 15))
        with self.assertRaises(AccountNotFound):
            self.events.withdraw(WithdrawDTO("200", 10))
        self.assertEqual(len(self.transactions.list_all()), 3)


class ResetTest(ServiceTestCase):
    def test_clears_accounts_and_transactions(self):
        self.events.deposit(DepositDTO("100", 10))
        self.resets.reset()
        self.assertIsNone(self.accounts.get("100"))
        self.assertEqual(self.transactions.list_all(), [])
