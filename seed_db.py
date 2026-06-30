import sqlite3
import random
from datetime import datetime, timedelta
import os
import sys

# اضافه کردن مسیر ریشه پروژه برای شناسایی ماژول‌ها
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.security_utils import hash_text

DB_NAME = "fund_database.db"


def seed_database():
    print("🌱 در حال تولید داده‌های تستی برای سامانه بانکی...")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # پاکسازی داده‌های قبلی مشتریان برای جلوگیری از تداخل (ادمین پاک نمی‌شود)
    cursor.execute("DELETE FROM Transactions")
    cursor.execute("DELETE FROM Accounts")
    cursor.execute("DELETE FROM Users")

    names = [
        "علی احمدی", "مریم رضایی", "حسین کریمی", "فاطمه موسوی", "رضا رحمانی",
        "سارا نجفی", "محمد حسینی", "زهرا قاسمی", "امیر نوری", "ندا طاهری"
    ]

    # تنظیم یک رمز عبور پیش‌فرض برای تمام کارت‌های تستی جهت راحتی در تست
    default_pin_hash = hash_text("1234")
    default_salt = "seed_salt_xyz"

    for name in names:
        # ۱. ساخت مشتری با کدملی و شماره تماس تصادفی
        national_id = f"00{random.randint(10000000, 99999999)}"
        phone = f"0912{random.randint(1000000, 9999999)}"
        # تاریخ عضویت تصادفی در ۱۰۰ روز گذشته
        created_at = (datetime.now() - timedelta(days=random.randint(1, 100))).strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute('''
                       INSERT INTO Users (name, national_id, phone, created_at)
                       VALUES (?, ?, ?, ?)
                       ''', (name, national_id, phone, created_at))
        user_id = cursor.lastrowid

        # ۲. ساخت حساب بانکی
        account_number = f"603799{random.randint(1000000000, 9999999999)}"
        # موجودی تصادفی بین ۱ تا ۵۰ میلیون تومان
        balance = random.randint(10, 500) * 100000

        cursor.execute('''
                       INSERT INTO Accounts (account_number, user_id, pin, salt, balance, status, created_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?)
                       ''', (account_number, user_id, default_pin_hash, default_salt, balance, "فعال", created_at))

        # ۳. ساخت چند تراکنش اولیه برای پر شدن تاریخچه و داشبورد
        for _ in range(random.randint(2, 5)):
            tx_amount = random.randint(1, 5) * 100000
            tx_type = random.choice(["واریز", "برداشت", "کارت به کارت"])
            # تاریخ تراکنش تصادفی
            tx_date = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute('''
                           INSERT INTO Transactions (account_number, transaction_type, amount, resulting_balance,
                                                     timestamp, description)
                           VALUES (?, ?, ?, ?, ?, ?)
                           ''', (account_number, tx_type, tx_amount, balance, tx_date,
                                 f"تراکنش تستی ایجاد شده توسط سیستم ({tx_type})"))

    conn.commit()
    conn.close()

    print("✅ دیتابیس با موفقیت با داده‌های استاندارد پر شد!")
    print("🔹 پین‌کد تمام حساب‌های تولید شده: 1234")


if __name__ == "__main__":
    seed_database()