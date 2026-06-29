import tkinter as tk
from tkinter import ttk, messagebox
from utils.text_normalizer import TextNormalizer
from widgets.tooltip import Tooltip


class BaseTab(ttk.Frame):
    """کلاس پایه برای تمام تب‌های رابط کاربری (ارث‌بری UI)"""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.PAD_SM, self.PAD_MD, self.PAD_LG = 10, 20, 30
        self.build_ui()

    def build_ui(self):
        pass

    def clear_form(self):
        pass

    def create_numeric_var(self, use_commas=False):
        var = tk.StringVar()

        def callback(*args):
            raw = var.get()
            if not raw: return
            clean = TextNormalizer.normalize_digits(raw, use_commas)
            filtered = ''.join([c for c in clean if c.isdigit()])
            formatted = f"{int(filtered):,}" if use_commas and filtered else filtered
            if raw != formatted: var.set(formatted)

        var.trace_add("write", callback)
        return var

    def create_form_row(self, parent, label_text, row_idx, var=None, is_pw=False, tip="", enter_func=None):
        # این ستون کشسانی کل فرم را به سمت راست هدایت می‌کند (RTL مادری)
        parent.columnconfigure(0, weight=1)

        # عنوان فیلد در سمت راست
        ttk.Label(parent, text=label_text).grid(row=row_idx, column=3, sticky="e", pady=self.PAD_SM, padx=5)

        # فیلد متنی با استارت تایپ راست‌چین
        entry = ttk.Entry(parent, textvariable=var, width=25, justify="right", font=("Samim", 11))
        entry.grid(row=row_idx, column=2, pady=self.PAD_SM, sticky="e")

        if enter_func: entry.bind("<Return>", lambda e: enter_func())

        # دکمه چشم برای نمایش پسورد
        if is_pw:
            entry.config(show="*")
            btn = ttk.Button(parent, text="👁", width=3,
                             command=lambda: entry.config(show="" if entry.cget("show") == "*" else "*"))
            btn.grid(row=row_idx, column=1, padx=5, sticky="w")
            if tip: Tooltip(btn, tip)

        return entry

    def validate_fields(self, *entries):
        is_valid = True
        for entry in entries:
            val = entry.get().strip()
            if not val:
                entry.configure(style="Error.TEntry")
                is_valid = False
            else:
                entry.configure(style="TEntry")
        return is_valid

    def wrap_action(self, button, func):
        def wrapper():
            button.state(["disabled"])
            self.update_idletasks()
            try:
                func()
            finally:
                if button.winfo_exists(): button.state(["!disabled"])

        return wrapper

    def ask_heavy_transaction(self, amount_str):
        clean_amt = amount_str.replace(',', '')
        if clean_amt.isdigit() and int(clean_amt) >= 5000000:
            return messagebox.askyesno("هشدار", "مبلغ تراکنش بالا است! آیا اطمینان دارید؟")
        return True