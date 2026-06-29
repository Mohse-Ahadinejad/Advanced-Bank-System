from .base_controller import BaseController
from model.account import Account
from model.transaction import TransferOut, TransferIn
from utils.security_utils import verify_pin


class TransferController(BaseController):
    def handle_transfer(self, src_num, dst_num, amount_str, pin):
        try:
            if src_num == dst_num:
                raise ValueError("حساب مبدأ و مقصد نمی‌تواند یکسان باشد.")

            amt = int(amount_str.replace(',', ''))
            if amt <= 0: raise ValueError("مبلغ وارد شده نامعتبر است.")

            src_data = self.repo.get_account_data(src_num)
            dst_data = self.repo.get_account_data(dst_num)

            if not src_data: raise ValueError("حساب مبدأ در سیستم یافت نشد.")
            if not dst_data: raise ValueError("حساب مقصد در سیستم یافت نشد.")

            if not verify_pin(pin, src_data['pin_hash'], src_data['salt']):
                self.log_action("SECURITY_ALERT", f"رمز اشتباه برای انتقال از حساب {src_num}", "WARNING")
                raise ValueError("رمز حساب مبدأ اشتباه است.")

            src_acc = Account(**src_data)
            dst_acc = Account(**dst_data)

            t_out = TransferOut(amt, dst_num)
            t_in = TransferIn(amt, src_num)

            # بررسی منطق دامنه روی هر دو حساب به صورت جداگانه (بدون ذخیره در دیتابیس)
            src_acc.apply_transaction(t_out)
            dst_acc.apply_transaction(t_in)

            # ثبت قطعی و همزمان هر دو تراکنش در دیتابیس (رول‌بک در صورت بروز خطا)
            self.repo.execute_atomic_transfer(src_acc, dst_acc, t_out, t_in)

            self.log_action("TRANSFER", f"انتقال مبلغ {amt} از {src_num} به {dst_num}")
            self.view.show_message("موفق", f"مبلغ {amt:,} ریال با موفقیت منتقل شد.")
            self.view.transfer_tab.clear_form()
            self.refresh_dashboard_data()
        except Exception as e:
            self.handle_error(e)