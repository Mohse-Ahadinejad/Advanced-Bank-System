from .base_controller import BaseController
from model.account import Account
from model.transaction import Deposit, Withdrawal
from utils.security_utils import verify_pin


class DepositWithdrawController(BaseController):
    def handle_deposit(self, acc_num, amount_str):
        try:
            amt = int(amount_str.replace(',', ''))
            if amt <= 0: raise ValueError("مبلغ وارد شده نامعتبر است.")

            acc_data = self.repo.get_account_data(acc_num)
            if not acc_data: raise ValueError("شماره حساب در سیستم یافت نشد.")

            acc = Account(**acc_data)
            dep = Deposit(amt)
            acc.apply_transaction(dep)  # اعمال منطق دامنه (بررسی وضعیت مسدودی)

            self.repo.execute_atomic_operation(acc, dep)
            self.log_action("DEPOSIT", f"واریز مبلغ {amt} به حساب {acc_num}")
            self.view.show_message("موفق", f"مبلغ {amt:,} ریال با موفقیت واریز شد.")
            self.view.deposit_tab.clear_form()
            self.refresh_dashboard_data()
        except Exception as e:
            self.handle_error(e)

    def handle_withdraw(self, acc_num, amount_str, pin):
        try:
            amt = int(amount_str.replace(',', ''))
            if amt <= 0: raise ValueError("مبلغ وارد شده نامعتبر است.")

            acc_data = self.repo.get_account_data(acc_num)
            if not acc_data: raise ValueError("شماره حساب در سیستم یافت نشد.")

            if not verify_pin(pin, acc_data['pin_hash'], acc_data['salt']):
                self.log_action("SECURITY_ALERT", f"رمز اشتباه برای برداشت از حساب {acc_num}", "WARNING")
                raise ValueError("رمز حساب اشتباه است.")

            acc = Account(**acc_data)
            wd = Withdrawal(amt)
            acc.apply_transaction(wd)  # اعمال منطق کسر وجه و بررسی موجودی کافی

            self.repo.execute_atomic_operation(acc, wd)
            self.log_action("WITHDRAW", f"برداشت مبلغ {amt} از حساب {acc_num}")
            self.view.show_message("موفق", f"مبلغ {amt:,} ریال با موفقیت برداشت شد.")
            self.view.deposit_tab.clear_form()
            self.refresh_dashboard_data()
        except Exception as e:
            self.handle_error(e)