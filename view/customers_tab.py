import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkfont
from .base_tab import BaseTab


class CustomersTab(BaseTab):
    def build_ui(self):
        self._sort_st = {}
        fs = ttk.Frame(self, padding=self.PAD_SM)
        fs.pack(fill="x")
        self.v_q = tk.StringVar()
        ttk.Label(fs, text="جستجوی هوشمند:").pack(side="right", padx=5)
        ttk.Entry(fs, textvariable=self.v_q, justify="right").pack(side="right", fill="x", expand=True)
        self.v_q.trace_add("write", lambda *a: self.controller.handle_customer_search(self.v_q.get()))

        ft = ttk.Frame(self, padding=self.PAD_SM)
        ft.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(ft, columns=("status", "created_at", "balance", "acc_num", "national_id", "name"),
                                 show="headings", selectmode="browse")
        cols = {"status": "وضعیت", "created_at": "تاریخ افتتاح", "balance": "موجودی (ریال)", "acc_num": "شماره حساب",
                "national_id": "کد ملی", "name": "نام و نام خانوادگی"}

        for c, t in cols.items():
            self._sort_st[c] = False
            self.tree.heading(c, text=t, command=lambda c_=c: self.sort_t(c_))

        self.tree.column("status", anchor="center", stretch=False)
        self.tree.column("created_at", anchor="center", stretch=False)
        self.tree.column("balance", anchor="center", stretch=False)
        self.tree.column("acc_num", anchor="center", stretch=False)
        self.tree.column("national_id", anchor="center", stretch=False)
        self.tree.column("name", anchor="e", stretch=True)

        self.tree.tag_configure("active", foreground="#1a7f37")
        self.tree.tag_configure("blocked", foreground="#b45309")
        self.tree.tag_configure("closed", foreground="#b91c1c", font=("Samim", 11, "overstrike"))
        self.tree.tag_configure("oddrow", background="#f7f7f7")
        self.tree.tag_configure("evenrow", background="#ffffff")

        self.tree.bind("<Double-1>", self.on_dc)
        scr = ttk.Scrollbar(ft, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scr.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scr.pack(side="right", fill="y")

        fa = ttk.LabelFrame(self, text=" عملیات مدیریت روی حساب انتخاب شده ", padding=self.PAD_SM, labelanchor="ne")
        fa.pack(fill="x", padx=15, pady=10)

        f1 = ttk.Frame(fa);
        f1.pack(fill="x", pady=5)
        ttk.Button(f1, text="ابطال (حذف) حساب", command=lambda: self.chg("بسته")).pack(side="right", padx=5,
                                                                                       expand=True, fill="x")
        ttk.Button(f1, text="مسدود کردن", command=lambda: self.chg("مسدود")).pack(side="right", padx=5, expand=True,
                                                                                  fill="x")
        ttk.Button(f1, text="رفع مسدودیت", command=lambda: self.chg("فعال")).pack(side="right", padx=5, expand=True,
                                                                                  fill="x")

        f2 = ttk.Frame(fa);
        f2.pack(fill="x", pady=5)
        ttk.Button(f2, text="نمایش صورت‌حساب", command=lambda: self.controller.handle_report(self.get_acc())).pack(
            side="right", padx=5, expand=True, fill="x")
        ttk.Button(f2, text="خروجی اکسل (CSV)", command=lambda: self.controller.handle_export_csv(self.get_acc())).pack(
            side="right", padx=5, expand=True, fill="x")

    def get_acc(self):
        s = self.tree.selection()
        if not s: messagebox.showerror("خطا", "ابتدا یک حساب را از جدول انتخاب کنید.")
        return str(self.tree.item(s)['values'][3]) if s else None

    def on_dc(self, e):
        a = self.get_acc()
        if a:
            main_view = self.controller.view
            main_view.deposit_tab.v_acc.set(a)
            main_view.transfer_tab.v_snd.set(a)
            main_view.nb.select(main_view.deposit_tab)
            main_view.status.config(text=f"حساب {a} جهت تراکنش بارگذاری شد.")

    def chg(self, st):
        a = self.get_acc()
        if a and (st != "بسته" or messagebox.askyesno("هشدار", "آیا از ابطال و حذف منطقی این حساب مطمئنید؟")):
            self.controller.handle_account_status_modify(a, st)

    def sort_t(self, col):
        rev = self._sort_st[col]
        cn = {"status": "وضعیت", "created_at": "تاریخ افتتاح", "balance": "موجودی (ریال)", "acc_num": "شماره حساب",
              "national_id": "کد ملی", "name": "نام و نام خانوادگی"}
        for c in self.tree["columns"]: self.tree.heading(c, text=cn[c])
        self.tree.heading(col, text=cn[col] + (" ▼" if rev else " ▲"))
        self._sort_st[col] = not rev
        l = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        if col == "balance":
            l.sort(key=lambda t: int(t[0].replace(',', '')), reverse=rev)
        else:
            l.sort(reverse=rev)
        for idx, (v, k) in enumerate(l): self.tree.move(k, '', idx)
        self.zebra()

    def update_tree_data(self, data):
        self.tree.delete(*self.tree.get_children())

        measure_font = tkfont.Font(family="Samim", size=11)
        headers = {"status": "وضعیت", "created_at": "تاریخ افتتاح", "balance": "موجودی (ریال)", "acc_num": "شماره حساب",
                   "national_id": "کد ملی", "name": "نام و نام خانوادگی"}
        col_widths = {col: measure_font.measure(text) + 30 for col, text in headers.items()}
        max_widths = {"status": 100, "created_at": 180, "balance": 200, "acc_num": 130, "national_id": 130, "name": 400}

        for r in data:
            tag = "blocked" if r[0] == "مسدود" else "closed" if r[0] == "بسته" else "active"
            safe_name = f"   {r[5]}   "
            vals = (r[0], r[1], f"{int(r[2]):,}", r[3], r[4], safe_name)
            self.tree.insert("", tk.END, values=vals, tags=(tag,))

            col_names = ["status", "created_at", "balance", "acc_num", "national_id", "name"]
            for i, col in enumerate(col_names):
                padding = 50 if col == "name" else 30
                txt_width = measure_font.measure(str(vals[i])) + padding
                if txt_width > col_widths[col]:
                    col_widths[col] = txt_width

        for col in self.tree["columns"]:
            final_width = min(col_widths[col], max_widths[col])
            is_stretch = True if col == "name" else False
            self.tree.column(col, width=final_width, stretch=is_stretch)

        self.zebra()

    def zebra(self):
        for i, item in enumerate(self.tree.get_children()):
            t = list(self.tree.item(item, "tags"))
            t = [x for x in t if x not in ("oddrow", "evenrow")]
            t.append("oddrow" if i % 2 != 0 else "evenrow")
            self.tree.item(item, tags=t)