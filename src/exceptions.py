class AccountNotFoundError(Exception):
    pass

class InsufficientFundsError(Exception):
    pass

class AccountClosedError(Exception):
    pass

class DuplicateAccountError(Exception):
    pass