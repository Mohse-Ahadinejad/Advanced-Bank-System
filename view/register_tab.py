import tkinter as tk
from tkinter import ttk
from .base_tab import BaseTab


class RegisterTab(BaseTab):
    def build_ui(self):
        f = ttk.LabelFrame(self, text=" افتتاح حساب مشتری جدید ", padding=self.PAD_MD, labelanchor="ne")
        f.pack(pady=self.PAD_LG, fill="x", padx=40)

        self.e_name = self.create_form_row(f, "نام و نام خانوادگی:", 0)
        self.v_nid = self.create_numeric_var()
        self.e_nid = self.create_form_row(f, "کد ملی:", 1, self.v_nid)
        self.v_phone = self.create_numeric_var()
        self.e_phone = self.create_form_row(f, "تلفن همراه:", 2, self.v_phone)
        self.v_pin = self.create_numeric_var()

        self.e_pin = self.create_form_row(f, "رمز حساب (۴ رقم):", 3, self.v_pin, True, enter_func=self.submit)

        self.btn = ttk.Button(f, text="صدور و افتتاح حساب", command=self.submit, width=20)
        self.btn.grid(row=4, column=1, columnspan=3, pady=self.PAD_MD)

    def submit(self):
        if not self.validate_fields(self.e_name, self.e_nid, self.e_phone, self.e_pin): return
        self.wrap_action(self.btn, lambda: self.controller.handle_register(self.e_name.get(), self.v_nid.get(),
                                                                           self.v_phone.get(), self.v_pin.get()))()

    def clear_form(self):
        self.e_name.delete(0, tk.END)
        self.v_nid.set("");
        self.v_phone.set("");
        self.v_pin.set("")
        for e in [self.e_name, self.e_nid, self.e_phone, self.e_pin]: e.configure(style="TEntry")