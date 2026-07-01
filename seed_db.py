import os
import random
from datetime import datetime, timedelta
from model.repository import BankRepository
from utils.security_utils import hash_pin


def seed_database():
    db_name = "fund_database.db"

    # ۱. پاکسازی دیتابیس قدیمی
    if os.path.exists(db_name):
        os.remove(db_name)
        print("🗑️  Old database removed.")

    repo = BankRepository(db_name=db_name)
    print("✨ New database initialized.")

    # ۲. اطلاعات ۱۲ مشتری واقع‌گرایانه
    users_data = [
        ("علی احمدی", "1111111111", "09121111111", "10000001", "فعال"),
        ("مریم رضایی", "2222222222", "09122222222", "10000002", "فعال"),
        ("سارا کریمی", "3333333333", "09123333333", "10000003", "مسدود"),
        ("رضا مرادی", "4444444444", "09124444444", "10000004", "فعال"),
        ("ندا رحیمی", "5555555555", "09125555555", "10000005", "فعال"),
        ("محمد حسینی", "6666666666", "09126666666", "10000006", "فعال"),
        ("فاطمه طاهری", "7777777777", "09127777777", "10000007", "فعال"),
        ("امیر قاسمی", "8888888888", "09128888888", "10000008", "بسته"),
        ("زهرا موسوی", "9999999999", "09129999999", "10000009", "فعال"),
        ("حسین عباسی", "1010101010", "09121010101", "10000010", "فعال"),
        ("مینا صالحی", "2020202020", "09122020202", "10000011", "فعال"),
        ("مهدی نجفی", "3030303030", "09123030303", "10000012", "فعال"),
    ]

    print("👥 Creating 12 customers with historical creation dates...")
    account_balances = {}

    for name, nid, phone, acc_num, status in users_data:
        # تاریخ افتتاح حساب: بین ۳۰ تا ۹۰ روز پیش
        created_days_ago = random.randint(30, 90)
        created_at = (datetime.now() - timedelta(days=created_days_ago)).strftime("%Y-%m-%d %H:%M:%S")

        user_id = repo.add_customer(name, nid, phone, created_at)
        pin_hash, salt = hash_pin("1234")
        repo.add_account(acc_num, user_id, pin_hash, salt, 0, status, created_at)
        account_balances[acc_num] = 0  # موجودی اولیه در حافظه برای محاسبه دقیق

    print("💸 Generating massive historical data (10-20 tx per account)...")

    # ۳. تزریق مستقیم اطلاعات به دیتابیس برای دستکاری زمان (Spoofing)
    with repo._get_connection() as conn:
        cursor = conn.cursor()

        for acc_num in account_balances.keys():
            # تولید بین ۱۰ تا ۲۰ تراکنش برای هر حساب
            num_tx = random.randint(10, 20)

            for i in range(num_tx):
                # تاریخ تراکنش: رندوم در ۳۰ روز گذشته
                days_ago = random.randint(1, 29)
                time_offset = timedelta(days=days_ago, hours=random.randint(1, 23), minutes=random.randint(1, 59))
                tx_date = (datetime.now() - time_offset).strftime("%Y-%m-%d %H:%M:%S")

                # برای جلوگیری از منفی شدن موجودی، اگر پول کم بود حتماً واریز می‌کنیم
                if account_balances[acc_num] < 500000 or random.random() < 0.4:
                    amt = random.randint(5, 50) * 100000  # مبلغ بین 500 هزار تا 5 میلیون
                    account_balances[acc_num] += amt
                    cursor.execute('''
                                   INSERT INTO Transactions (account_number, transaction_type, amount,
                                                             resulting_balance, timestamp, description)
                                   VALUES (?, ?, ?, ?, ?, ?)
                                   ''', (acc_num, "واریز نقدی", amt, account_balances[acc_num], tx_date,
                                         "واریز وجه به صندوق"))

                elif random.random() < 0.5:
                    amt = random.randint(1, 4) * 100000
                    account_balances[acc_num] -= amt
                    cursor.execute('''
                                   INSERT INTO Transactions (account_number, transaction_type, amount,
                                                             resulting_balance, timestamp, description)
                                   VALUES (?, ?, ?, ?, ?, ?)
                                   ''', (acc_num, "برداشت نقدی", amt, account_balances[acc_num], tx_date,
                                         "برداشت نقدی از حساب"))

                else:
                    # انتقال وجه رندوم به یک حساب دیگر
                    target = random.choice([a for a in account_balances.keys() if a != acc_num])
                    amt = random.randint(1, 5) * 100000

                    # کسر از مبدأ
                    account_balances[acc_num] -= amt
                    cursor.execute('''
                                   INSERT INTO Transactions (account_number, transaction_type, amount,
                                                             resulting_balance, timestamp, description)
                                   VALUES (?, ?, ?, ?, ?, ?)
                                   ''', (acc_num, "انتقال (خروجی)", amt, account_balances[acc_num], tx_date,
                                         f"انتقال وجه به {target}"))

                    # واریز به مقصد
                    account_balances[target] += amt
                    cursor.execute('''
                                   INSERT INTO Transactions (account_number, transaction_type, amount,
                                                             resulting_balance, timestamp, description)
                                   VALUES (?, ?, ?, ?, ?, ?)
                                   ''', (target, "انتقال (ورودی)", amt, account_balances[target], tx_date,
                                         f"واریز از حساب {acc_num}"))

        # ۴. آپدیت کردن موجودی نهایی تمام حساب‌ها در دیتابیس
        for acc_num, final_balance in account_balances.items():
            cursor.execute('UPDATE Accounts SET balance = ? WHERE account_number = ?', (final_balance, acc_num))

        conn.commit()

    print("\n✅ Database seeding completed successfully with rich historical data!")
    print("   🔑 Admin Login -> User: admin | Pass: 12345")
    print("   💳 Default PIN for all test accounts: 1234")


if __name__ == "__main__":
    seed_database()