import tkinter as tk
from tkinter import ttk
from .base_tab import BaseTab


class DepositWithdrawTab(BaseTab):
    def build_ui(self):
        f = ttk.LabelFrame(self, text=" عملیات بانکی مستقیم ", padding=self.PAD_MD, labelanchor="ne")
        f.pack(pady=self.PAD_LG, fill="x", padx=40)
        self.v_acc = self.create_numeric_var()
        self.e_acc = self.create_form_row(f, "شماره حساب مشتری:", 0, self.v_acc)

        self.v_amt = self.create_numeric_var(True)
        self.e_amt = self.create_form_row(f, "مبلغ (ریال):", 1, self.v_amt)

        self.v_pin = self.create_numeric_var()
        self.e_pin = self.create_form_row(f, "رمز حساب (برای برداشت):", 2, self.v_pin, True, tip="نمایش/مخفی",
                                          enter_func=self.do_with)

        fb = ttk.Frame(f)
        fb.grid(row=3, column=1, columnspan=3, pady=self.PAD_MD)
        self.b_dep = ttk.Button(fb, text="واریز وجه", command=self.do_dep, width=15);
        self.b_dep.pack(side="right", padx=10)
        self.b_with = ttk.Button(fb, text="برداشت نقدی", command=self.do_with, width=15);
        self.b_with.pack(side="left", padx=10)

    def do_dep(self):
        if not self.validate_fields(self.e_acc, self.e_amt): return
        self.wrap_action(self.b_dep, lambda: self.controller.handle_deposit(self.v_acc.get(), self.v_amt.get()))()

    def do_with(self):
        if not self.validate_fields(self.e_acc, self.e_amt, self.e_pin): return
        if not self.ask_heavy_transaction(self.v_amt.get()): return
        self.wrap_action(self.b_with, lambda: self.controller.handle_withdraw(self.v_acc.get(), self.v_amt.get(),
                                                                              self.v_pin.get()))()

    def clear_form(self):
        self.v_acc.set("");
        self.v_amt.set("");
        self.v_pin.set("")
        for e in [self.e_acc, self.e_amt, self.e_pin]: e.configure(style="TEntry")