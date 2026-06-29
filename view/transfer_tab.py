import tkinter as tk
from tkinter import ttk
from .base_tab import BaseTab

class TransferTab(BaseTab):
    def build_ui(self):
        f = ttk.LabelFrame(self, text=" انتقال وجه بین حساب‌ها ", padding=self.PAD_MD, labelanchor="ne")
        f.pack(pady=self.PAD_LG, fill="x", padx=40)
        self.v_snd = self.create_numeric_var()
        self.e_snd = self.create_form_row(f, "حساب مبدأ:", 0, self.v_snd)
        self.v_rec = self.create_numeric_var()
        self.e_rec = self.create_form_row(f, "حساب مقصد:", 1, self.v_rec)
        self.v_amt = self.create_numeric_var(True)
        self.e_amt = self.create_form_row(f, "مبلغ انتقال:", 2, self.v_amt)
        self.v_pin = self.create_numeric_var()
        self.e_pin = self.create_form_row(f, "رمز حساب مبدأ:", 3, self.v_pin, True, enter_func=self.submit)
        self.btn = ttk.Button(f, text="تایید و انتقال", command=self.submit, width=20)
        self.btn.grid(row=4, column=1, columnspan=3, pady=self.PAD_MD)

    def submit(self):
        if not self.validate_fields(self.e_snd, self.e_rec, self.e_amt, self.e_pin): return
        if not self.ask_heavy_transaction(self.v_amt.get()): return
        self.wrap_action(self.btn, lambda: self.controller.handle_transfer(self.v_snd.get(), self.v_rec.get(), self.v_amt.get(), self.v_pin.get()))()

    def clear_form(self):
        self.v_snd.set(""); self.v_rec.set(""); self.v_amt.set(""); self.v_pin.set("")
        for e in [self.e_snd, self.e_rec, self.e_amt, self.e_pin]: e.configure(style="TEntry")