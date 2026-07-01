class BankError(Exception):
    """کلاس پایه برای تمام خطاهای منطقی سیستم بانکی"""
    pass

class AccountBlockedError(BankError):
    """خطای مربوط به تلاش برای تراکنش روی حساب مسدود شده"""
    pass

class AccountClosedError(BankError):
    """خطای مربوط به تلاش برای تراکنش روی حساب بسته شده (ابطال شده)"""
    pass

class InsufficientBalanceError(BankError):
    """خطای مربوط به ناکافی بودن موجودی برای برداشت یا انتقال"""
    pass

class InvalidPinError(BankError):
    """خطای مربوط به اشتباه بودن رمز عبور (پین‌کد) حساب"""
    pass