from .exceptions import InsufficientFundsError, AccountFrozenError

class Account:
    def __init__(self, account_id, holder_name, balance=0.0, interest_rate=5):
        self.account_id = account_id
        self.holder_name = holder_name
        self.balance = float(balance)
        self.interest_rate = interest_rate
        self.is_frozen = False
        self._is_frozen = False

    def deposit(self, amount):
        if self.is_frozen or self._is_frozen:
            raise AccountFrozenError("Account is frozen")
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        if self.is_frozen or self._is_frozen:
            raise AccountFrozenError("Account is frozen")
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if amount > self.balance:
            raise InsufficientFundsError("Insufficient funds")
        self.balance -= amount
        return self.balance

    def freeze(self):
        self.is_frozen = True
        self._is_frozen = True

    def unfreeze(self):
        self.is_frozen = False
        self._is_frozen = False

    def to_dict(self):
        return {
            "account_id": self.account_id,
            "holder_name": self.holder_name,
            "balance": self.balance,
            "type": self.__class__.__name__,
            "interest_rate": self.interest_rate
        }

    def calculate_interest(self):
        return self.balance * self.interest_rate / 100

# Alias for backward compatibility
BankAccount = Account

class SavingsAccount(Account):
    def __init__(self, account_id, holder_name, balance=0.0, interest_rate=5):
        super().__init__(account_id, holder_name, balance, interest_rate)

class CheckingAccount(Account):
    def __init__(self, account_id, holder_name, balance=0.0, overdraft_limit=500):
        super().__init__(account_id, holder_name, balance, 0)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if self.is_frozen or self._is_frozen:
            raise AccountFrozenError("Account is frozen")
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if self.balance + self.overdraft_limit < amount:
            raise InsufficientFundsError("Overdraft limit exceeded")
        self.balance -= amount
        return self.balance

class FixedDepositAccount(Account):
    def __init__(self, account_id, holder_name, balance=0.0, interest_rate=7, tenure=12):
        super().__init__(account_id, holder_name, balance, interest_rate)
        self.tenure = tenure