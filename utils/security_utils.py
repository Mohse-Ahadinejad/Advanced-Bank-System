import hashlib
import secrets

def hash_text(text, salt="B@nkS3cur1ty_S@lt_9988"):
    """تولید هش امن با الگوریتم SHA-256"""
    return hashlib.sha256((text + salt).encode('utf-8')).hexdigest()

def hash_pin(pin):
    """هش کردن پین ۴ رقمی کاربر به همراه تولید یک Salt اختصاصی تصادفی"""
    salt = secrets.token_hex(8)
    pin_hash = hash_text(pin, salt=salt)
    return pin_hash, salt

def verify_pin(pin, pin_hash, salt):
    """بررسی صحت پین وارد شده با مقایسه با هش ذخیره شده"""
    return hash_text(pin, salt=salt) == pin_hash

def verify_password(password, stored_hash):
    """بررسی صحت رمز عبور ادمین سیستم"""
    return hash_text(password) == stored_hash