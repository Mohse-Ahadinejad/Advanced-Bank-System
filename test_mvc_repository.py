import os
import pytest
from model.repository import BankRepository
from utils.security_utils import hash_text


# ================= 1. Fixture Setup =================
@pytest.fixture
def repo():
    """یک دیتابیس تستی ایزوله می‌سازد و بعد از پایان تست آن را پاک می‌کند"""
    test_db = "test_mvc_bank_system.db"
    repository = BankRepository(db_name=test_db)

    yield repository

    # پاکسازی فایل دیتابیس تستی بعد از اتمام تست‌ها
    if os.path.exists(test_db):
        os.remove(test_db)


# ================= 2. Database Initialization Tests =================
def test_database_initialization_and_admin_creation(repo):
    """بررسی ساخته شدن جداول و ادمین پیش‌فرض در دیتابیس جدید"""
    admin_hash = repo.get_admin_password_hash("admin")
    assert admin_hash is not None, "ادمین پیش‌فرض باید به صورت خودکار ساخته شود"


# ================= 3. Core CRUD Operations Tests =================
def test_add_customer_and_account(repo):
    """بررسی ثبت صحیح مشتری و متصل شدن حساب به آن"""
    user_id = repo.add_customer("تست کاربر", "0123456789", "09120000000")
    assert user_id > 0

    customer = repo.get_customer_by_nid("0123456789")
    assert customer is not None
    assert customer[1] == "تست کاربر"

    pin_hash, salt = hash_text("1234"), "test_salt"
    repo.add_account("6037990000000000", user_id, pin_hash, salt, 500000, "فعال")

    acc_data = repo.get_account_data("6037990000000000")
    assert acc_data is not None
    assert acc_data["balance"] == 500000
    assert acc_data["status"] == "فعال"


# ================= 4. Regression Test (The 6-Column Bug) =================
def test_search_customers_returns_exactly_6_columns(repo):
    """
    رگرسیون تست: تضمین می‌کند که خروجی جستجو دقیقاً ۶ آیتم برای پر کردن Treeview دارد
    و ترتیب آن‌ها دقیقاً مطابق با انتظار UI است.
    """
    user_id = repo.add_customer("مشتری گزارش", "9998887776", "09129998877")
    repo.add_account("1111222233334444", user_id, "hash", "salt", 1000, "فعال")

    results = repo.search_customers("مشتری گزارش")

    assert len(results) == 1, "باید یک مشتری پیدا شود"
    assert len(results[0]) == 6, "خروجی دیتابیس باید دقیقاً ۶ ستون برای رابط کاربری داشته باشد"

    # 🎯 اصلاح حیاتی: ترتیب دریافت خروجی‌ها دقیقاً با کوئری دیتابیس هماهنگ شد
    # خروجی دیتابیس تو: status, created_at, balance, account_number, national_id, name
    status, created_at, balance, acc_num, nid, name = results[0]

    assert status == "فعال"
    assert name == "مشتری گزارش"
    assert nid == "9998887776"
    assert acc_num == "1111222233334444"


# ================= 5. Dashboard Stats Tests =================
def test_dashboard_stats_calculation(repo):
    """بررسی محاسبه درست آمارهای داشبورد"""
    u1 = repo.add_customer("کاربر یک", "111", "091")
    repo.add_account("1001", u1, "h", "s", 150000, "فعال")

    u2 = repo.add_customer("کاربر دو", "222", "092")
    repo.add_account("1002", u2, "h", "s", 350000, "فعال")

    u3 = repo.add_customer("کاربر سه", "333", "093")
    repo.add_account("1003", u3, "h", "s", 999999, "بسته")

    stats = repo.get_dashboard_stats()

    assert stats["total_members"] == 2
    assert stats["total_assets"] == 500000