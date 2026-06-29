import tkinter as tk
from tkinter import ttk
from .base_tab import BaseTab


class DashboardTab(BaseTab):
    def build_ui(self):
        fc = ttk.Frame(self, padding=self.PAD_MD)
        fc.pack(fill="x", expand=True)
        cards = [(" 👥 اعضای شبکه ", "کل مشتریان:", "lbl_mem"), (" 💰 تراز مالی ", "سرمایه کل (ریال):", "lbl_ast"),
                 (" 📊 نرخ تراکنش‌ها ", "تراکنش‌های امروز:", "lbl_tx")]
        for title, label, attr in cards:
            c = ttk.LabelFrame(fc, text=title, padding=15, labelanchor="ne")
            c.pack(fill="x", pady=self.PAD_SM)
            ttk.Label(c, text=label, style="CardTitle.TLabel").pack(anchor="e")
            l = ttk.Label(c, text="۰", style="CardValue.TLabel")
            l.pack(anchor="e")
            setattr(self, attr, l)

    def update_data(self, s):
        trans = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')
        self.lbl_mem.config(text=str(s["total_members"]).translate(trans))
        self.lbl_ast.config(text=f'{int(s["total_assets"]):,}'.translate(trans))
        self.lbl_tx.config(text=str(s["today_transactions"]).translate(trans))