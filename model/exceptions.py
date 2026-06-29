class BankError(Exception):
    """کلاس پایه برای تمام خطاهای دامنه سیستم بانکی"""
    pass

class InsufficientBalanceError(BankError):
    """موجودی حساب برای انجام تراکنش کافی نیست"""
    pass

class InvalidPinError(BankError):
    """رمز وارد شده نامعتبر است"""
    pass

class AccountBlockedError(BankError):
    """حساب مسدود یا بسته است و اجازه تراکنش ندارد"""
    pass

class AccountNotFoundError(BankError):
    """حساب در پایگاه داده یافت نشد"""
    pass
