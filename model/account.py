from .exceptions import AccountBlockedError


class Account:
    """موجودیت حساب بانکی و مدیریت وضعیت آن"""

    def __init__(self, account_number, user_id=None, pin_hash=None, salt=None, balance=0, status="فعال",
                 created_at=None):
        self.account_number = account_number
        self.user_id = user_id
        self.pin_hash = pin_hash
        self.salt = salt
        self.balance = balance
        self.status = status
        self.created_at = created_at

    def apply_transaction(self, transaction):
        """
        اعمال تراکنش روی حساب با استفاده از Duck Typing
        بدون import کردن مستقیم کلاس‌های تراکنش برای جلوگیری از وابستگی حلقوی.
        """
        if self.status != "فعال":
            raise AccountBlockedError(f"حساب {self.account_number} در وضعیت '{self.status}' است و امکان تراکنش ندارد.")

        # متد execute در شیء تراکنش پیاده‌سازی شده است
        transaction.execute(self)