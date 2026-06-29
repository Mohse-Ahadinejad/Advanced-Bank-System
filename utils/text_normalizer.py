class TextNormalizer:
    @staticmethod
    def normalize_digits(text, use_commas=False):
        """تبدیل کاراکترهای عددی فارسی و عربی به معادل استاندارد انگلیسی"""
        persian_digits = '۰۱۲۳۴۵۶۷۸۹'
        arabic_digits = '٠١٢٣٤٥٦٧٨٩'
        english_digits = '0123456789'

        translation_table = str.maketrans(persian_digits + arabic_digits, english_digits * 2)
        clean_text = text.translate(translation_table)
        return clean_text