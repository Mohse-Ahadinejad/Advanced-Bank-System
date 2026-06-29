import logging
from model.exceptions import BankError

# تنظیمات لاگ‌گیری استاندارد پایتون (سیستم Audit Trail)
logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')
logger = logging.getLogger("BankSystem")

class BaseController:
    """هماهنگ‌کننده‌ی اصلی: تامین دسترسی به دیتابیس، ویو و منطق‌های مشترک"""
    def __init__(self, repo, view):
        self.repo = repo
        self.view = view

    def refresh_dashboard_data(self):
        """متد مشترک برای آپدیت اعداد داشبورد (جلوگیری از تکرار کد)"""
        stats = self.repo.get_dashboard_stats()
        self.view.update_dashboard_labels(stats)

    def log_action(self, action_type, details, level="INFO"):
        """ثبت امن فعالیت‌های متصدی در فایل لاگ بدون نشت اطلاعات حساس"""
        log_msg = f"[{action_type}] {details}"
        if level == "ERROR":
            logger.error(log_msg)
        elif level == "WARNING":
            logger.warning(log_msg)
        else:
            logger.info(log_msg)

    def handle_error(self, error):
        """مدیریت یکپارچه استثناها و نمایش پیام مناسب به کاربر"""
        if isinstance(error, BankError):
            self.view.show_message("خطای عملیات", str(error), is_error=True)
            self.log_action("DOMAIN_ERROR", str(error), "WARNING")
        elif isinstance(error, ValueError):
            self.view.show_message("خطای ورودی", str(error), is_error=True)
            self.log_action("VALIDATION_ERROR", str(error), "WARNING")
        else:
            self.view.show_message("خطای سیستمی", f"یک خطای غیرمنتظره رخ داد: {str(error)}", is_error=True)
            self.log_action("SYSTEM_CRASH", str(error), "ERROR")