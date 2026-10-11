import pytest
import os
from banking_ledger import BankLedger
from banking_ledger.models import SavingsAccount
from banking_ledger.exceptions import InsufficientFundsError, AccountFrozenError

def test_deposit():
    l = BankLedger()
    l.create_account("savings", "S001", "Muneswari", 1000)
    l.deposit("S001", 500)
    assert l.get_account("S001").balance == 1500

def test_withdraw():
    l = BankLedger()
    l.create_account("savings", "S001", "M", 1000)
    l.withdraw("S001", 400)
    assert l.get_account("S001").balance == 600

def test_insufficient():
    l = BankLedger()
    l.create_account("savings", "S001", "M", 100)
    with pytest.raises(InsufficientFundsError):
        l.withdraw("S001", 500)

def test_transfer():
    l = BankLedger()
    l.create_account("savings", "S1", "A", 1000)
    l.create_account("checking", "C1", "B", 500)
    l.transfer("S1", "C1", 200)
    assert l.get_account("C1").balance == 700

def test_freeze():
    l = BankLedger()
    l.create_account("savings", "S1", "A", 1000)
    l.freeze_account("S1")
    with pytest.raises(AccountFrozenError):
        l.deposit("S1", 100)

def test_json():
    l = BankLedger()
    l.create_account("savings", "S1", "M", 1000)
    l.save_to_json("t.json")
    l2 = BankLedger()
    l2.load_from_json("t.json")
    assert l2.get_account("S1").balance == 1000
    os.remove("t.json")

def test_csv():
    l = BankLedger()
    l.create_account("savings", "S1", "M", 1000)
    l.export_csv("t.csv")
    l2 = BankLedger()
    l2.import_csv("t.csv")
    assert l2.get_account("S1").balance == 1000
    os.remove("t.csv")

def test_interest():
    s = SavingsAccount("S1", "A", 1000, 5)
    assert s.calculate_interest() == 50