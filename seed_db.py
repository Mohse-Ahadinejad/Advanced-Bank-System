import os
from model.repository import BankRepository
from model.account import Account
from model.transaction import Deposit, Withdrawal, TransferOut, TransferIn
from utils.security_utils import hash_pin


def seed_database():
    db_name = "fund_database.db"

    # ۱. پاک کردن دیتابیس قدیمی برای جلوگیری از تداخل اطلاعات و تست تمیز
    if os.path.exists(db_name):
        os.remove(db_name)
        print("🗑️  Old database removed.")

    # با صدا زدن ریپازیتوری، دیتابیس جدید به همراه مایگریشن و ادمین امن ساخته می‌شود
    repo = BankRepository(db_name=db_name)
    print("✨ New database and schema initialized.")

    # --- ۲. ساخت مشتریان و حساب‌های تستی ---
    # ساختار: (نام، کدملی، موبایل، شماره حساب، موجودی اولیه، وضعیت)
    users = [
        ("علی احمدی", "1111111111", "09121111111", "10000001", 5000000, "فعال"),
        ("مریم رضایی", "2222222222", "09122222222", "10000002", 1500000, "فعال"),
        ("سارا کریمی", "3333333333", "09123333333", "10000003", 0, "مسدود")
    ]

    accounts_objects = {}

    print("👥 Creating customers and accounts...")
    for name, nid, phone, acc_num, balance, status in users:
        user_id = repo.add_customer(name, nid, phone)

        # 🎯 اصلاح حیاتی: دریافت همزمان هش و سالت برای هر کارت
        pin_hash, salt = hash_pin("1234")

        repo.add_account(acc_num, user_id, pin_hash, salt, balance, status)

        # استخراج دیتای حساب و ساخت شیء Account برای ثبت تراکنش‌های بعدی
        acc_data = repo.get_account_data(acc_num)
        accounts_objects[acc_num] = Account(**acc_data)

    # --- ۳. ثبت چند تراکنش تستی در تاریخچه ---
    print("💸 Generating mock transactions...")

    acc_ali = accounts_objects["10000001"]
    acc_maryam = accounts_objects["10000002"]

    # تراکنش اول: واریز به حساب علی
    dep = Deposit(200000)
    acc_ali.apply_transaction(dep)  # عبور از فیلتر امنیتی دامنه
    repo.execute_atomic_operation(acc_ali, dep)

    # تراکنش دوم: برداشت از حساب علی
    wd = Withdrawal(50000)
    acc_ali.apply_transaction(wd)
    repo.execute_atomic_operation(acc_ali, wd)

    # تراکنش سوم: کارت به کارت از علی به مریم
    t_out = TransferOut(100000, acc_maryam.account_number)
    t_in = TransferIn(100000, acc_ali.account_number)

    acc_ali.apply_transaction(t_out)
    acc_maryam.apply_transaction(t_in)
    repo.execute_atomic_transfer(acc_ali, acc_maryam, t_out, t_in)

    print("\n✅ Database seeding completed successfully!")
    print("   🔑 Admin Login -> User: admin | Pass: 12345")
    print("   💳 Default PIN for all test accounts: 1234")


if __name__ == "__main__":
    seed_database()