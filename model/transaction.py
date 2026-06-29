from .exceptions import InsufficientBalanceError


class TransactionType:
    """کلاس پایه برای تمام تراکنش‌های بانکی"""

    def __init__(self, amount):
        self.amount = amount

    def execute(self, account):
        raise NotImplementedError("متد execute باید در کلاس‌های فرزند پیاده‌سازی شود.")

    def get_description(self):
        return "تراکنش نامشخص"

    def get_type_name(self):
        return "نامشخص"


class Deposit(TransactionType):
    def execute(self, account):
        account.balance += self.amount

    def get_description(self):
        return "واریز نقدی مستقیم"

    def get_type_name(self):
        return "واریز"


class Withdrawal(TransactionType):
    def execute(self, account):
        if account.balance < self.amount:
            raise InsufficientBalanceError("موجودی حساب برای این برداشت کافی نیست.")
        account.balance -= self.amount

    def get_description(self):
        return "برداشت نقدی از باجه"

    def get_type_name(self):
        return "برداشت"


class TransferOut(TransactionType):
    def __init__(self, amount, destination_acc):
        super().__init__(amount)
        self.destination_acc = destination_acc

    def execute(self, account):
        if account.balance < self.amount:
            raise InsufficientBalanceError("موجودی حساب برای انتقال وجه کافی نیست.")
        account.balance -= self.amount

    def get_description(self):
        return f"انتقال (خروجی) به حساب {self.destination_acc}"

    def get_type_name(self):
        return "انتقال (خروجی)"


class TransferIn(TransactionType):
    def __init__(self, amount, source_acc):
        super().__init__(amount)
        self.source_acc = source_acc

    def execute(self, account):
        account.balance += self.amount

    def get_description(self):
        return f"انتقال (ورودی) از حساب {self.source_acc}"

    def get_type_name(self):
        return "انتقال (ورودی)"