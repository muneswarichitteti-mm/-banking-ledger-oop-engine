import json
import csv
import os
from .models import SavingsAccount, CheckingAccount
from .exceptions import InsufficientFundsError, AccountFrozenError

class BankLedger:
    def __init__(self):
        self.accounts = {}

    def create_account(self, account_type, account_id, holder_name, balance=0.0, **kwargs):
        if account_id in self.accounts:
            raise ValueError("Account exists")
        if "savings" in account_type.lower():
            acc = SavingsAccount(account_id, holder_name, balance, kwargs.get('interest_rate', 5))
        else:
            acc = CheckingAccount(account_id, holder_name, balance, kwargs.get('overdraft_limit', 500))
        self.accounts[account_id] = acc
        return acc

    def get_account(self, account_id):
        if account_id not in self.accounts:
            raise ValueError("Not found")
        return self.accounts[account_id]

    def deposit(self, account_id, amount):
        return self.get_account(account_id).deposit(amount)

    def withdraw(self, account_id, amount):
        return self.get_account(account_id).withdraw(amount)

    def transfer(self, from_id, to_id, amount):
        self.withdraw(from_id, amount)
        self.deposit(to_id, amount)
        return True

    def freeze_account(self, account_id):
        self.get_account(account_id).freeze()

    def unfreeze_account(self, account_id):
        self.get_account(account_id).unfreeze()

    def to_dict(self):
        return {k: v.to_dict() for k, v in self.accounts.items()}

    def save_to_json(self, filepath="ledger.json"):
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)

    def load_from_json(self, filepath="ledger.json"):
        if not os.path.exists(filepath):
            return
        with open(filepath, 'r') as f:
            data = json.load(f)
            for aid, adata in data.items():
                self.create_account(adata.get('type','savings'), aid, adata['holder_name'], adata['balance'])

    def export_to_csv(self, filepath="t.csv"):
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['account_id', 'holder_name', 'balance', 'type'])
            for acc in self.accounts.values():
                writer.writerow([acc.account_id, acc.holder_name, acc.balance, acc.__class__.__name__])

    def export_csv(self, filepath="t.csv"):
        return self.export_to_csv(filepath)

    def import_csv(self, filepath="t.csv"):
        if not os.path.exists(filepath):
            return
        with open(filepath, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                acc_id = row['account_id']
                holder = row['holder_name']
                balance = float(row['balance'])
                acc_type = row['type']
                if acc_id not in self.accounts:
                    self.create_account(acc_type, acc_id, holder, balance)

    def export_transactions_csv(self, filepath="transactions.csv"):
        self.export_to_csv(filepath)
    
    def import_from_csv(self, filepath="t.csv"):
        return self.import_csv(filepath)