import csv
from .base_controller import BaseController


class CustomersController(BaseController):
    def handle_customer_search(self, query):
        data = self.repo.search_customers(query)
        self.view.customers_tab.update_tree_data(data)

    def handle_account_status_modify(self, acc_num, new_status):
        try:
            self.repo.update_account_status(acc_num, new_status)
            self.log_action("STATUS_CHANGE", f"وضعیت حساب {acc_num} به {new_status} تغییر یافت")
            self.view.show_message("موفق", f"وضعیت حساب به '{new_status}' تغییر کرد.")

            # رفرش کردن جدول مشتریان برای نمایش زنده تغییر رنگ
            self.handle_customer_search(self.view.customers_tab.v_q.get())
            self.refresh_dashboard_data()
        except Exception as e:
            self.handle_error(e)

    def handle_report(self, acc_num):
        records = self.repo.get_account_history(acc_num)
        self.view.show_history_window(acc_num, records)
        self.log_action("REPORT_VIEW", f"مشاهده تاریخچه حساب {acc_num}")

    def handle_export_csv(self, acc_num):
        records = self.repo.get_account_history(acc_num)
        if not records:
            self.view.show_message("خطا", "هیچ تراکنشی برای این حساب ثبت نشده است.", is_error=True)
            return

        filepath = self.view.ask_save_file(
            ext=".csv",
            init=f"BankReport_{acc_num}.csv",
            title="ذخیره گزارش اکسل",
            types=[("CSV files", "*.csv")]
        )

        if not filepath:  # کاربر کنسل کرده است
            return

        try:
            # استفاده از utf-8-sig برای پشتیبانی از کاراکترهای فارسی در اکسل ویندوز
            with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow(['نوع تراکنش', 'مبلغ (ریال)', 'موجودی پس از تراکنش', 'زمان', 'توضیحات'])
                for row in records:
                    writer.writerow(row)

            self.log_action("EXPORT_CSV", f"دریافت خروجی اکسل برای حساب {acc_num}")
            self.view.show_message("موفق", "فایل گزارش با موفقیت در سیستم شما ذخیره شد.")
        except Exception as e:
            self.handle_error(e)