class BankingError(Exception):
    pass
class InvalidAmountError(BankingError):
    pass
class InsufficientFundsError(BankingError):
    pass
class AccountFrozenError(BankingError):
    pass
