import random
from .base_controller import BaseController
from utils.security_utils import hash_pin


class RegisterController(BaseController):
    def handle_register(self, name, nid, phone, pin):
        try:
            if len(pin) != 4 or not pin.isdigit():
                raise ValueError("رمز حساب باید دقیقاً ۴ رقم باشد.")

            pin_hash, salt = hash_pin(pin)

            # بررسی وجود مشتری قدیمی یا ثبت مشتری جدید
            cust = self.repo.get_customer_by_nid(nid)
            user_id = cust[0] if cust else self.repo.add_customer(name, nid, phone)

            # تولید یک شماره حساب ۸ رقمی رندوم (شبیه‌ساز سیستم متمرکز)
            acc_num = str(random.randint(10000000, 99999999))

            self.repo.add_account(acc_num, user_id, pin_hash, salt)

            self.log_action("REGISTER_SUCCESS", f"افتتاح حساب {acc_num} برای کد ملی {nid}")
            self.view.show_message("موفق", f"حساب با شماره {acc_num} با موفقیت افتتاح شد.")
            self.view.register_tab.clear_form()
            self.refresh_dashboard_data()

        except Exception as e:
            self.handle_error(e)