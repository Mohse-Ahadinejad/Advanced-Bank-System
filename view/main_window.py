import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from .dashboard_tab import DashboardTab
from .customers_tab import CustomersTab
from .register_tab import RegisterTab
from .transfer_tab import TransferTab
from .deposit_withdraw_tab import DepositWithdrawTab


class BankView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("سامانه پیشرفته صندوق")
        self.geometry("900x700")
        self.configure(bg="#f0f0f0")

        self.auth_controller = None
        self.customers_controller = None
        self.register_controller = None
        self.transfer_controller = None
        self.deposit_withdraw_controller = None

        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabelframe", background="#f0f0f0")
        self.style.configure("TLabelframe.Label", background="#f0f0f0", font=("Samim", 11, "bold"))
        self.style.configure("TLabel", background="#f0f0f0")

        self.style.configure(".", font=("Samim", 11))
        self.style.configure("Header.TLabel", font=("Samim", 14, "bold"), foreground="#1a1a1a")
        self.style.configure("CardTitle.TLabel", font=("Samim", 11), foreground="#555555")
        self.style.configure("CardValue.TLabel", font=("Samim", 16, "bold"), foreground="#0078d4")
        self.style.configure("Error.TEntry", fieldbackground="#ffe6e6")
        self.style.configure("TEntry", fieldbackground="white")
        self.style.configure("TNotebook", tabposition="ne", background="#f0f0f0")
        self.style.configure("TNotebook.Tab", font=("Samim", 11))

        self.style.configure("Treeview", rowheight=30, font=("Samim", 11))
        self.style.configure("Treeview.Heading", font=("Samim", 11, "bold"), background="#e0e0e0")

    def wire_controllers(self, auth_ctrl, customers_ctrl, register_ctrl, transfer_ctrl, deposit_withdraw_ctrl):
        self.auth_controller = auth_ctrl
        self.customers_controller = customers_ctrl
        self.register_controller = register_ctrl
        self.transfer_controller = transfer_ctrl
        self.deposit_withdraw_controller = deposit_withdraw_ctrl

        self.protocol("WM_DELETE_WINDOW", self.auth_controller.handle_exit)
        self._build_login()

    def _build_login(self):
        self.f_login = ttk.Frame(self)
        self.f_login.pack(expand=True, fill="both")

        l_f = ttk.LabelFrame(self.f_login, text="", padding=30)
        l_f.place(relx=0.5, rely=0.45, anchor="center")

        ttk.Label(l_f, text="سامانه متمرکز صندوق", style="Header.TLabel").grid(row=0, columnspan=2, pady=(0, 20))

        ttk.Label(l_f, text="نام کاربری:").grid(row=1, column=1, sticky="e", pady=5, padx=5)
        self.e_user = ttk.Entry(l_f, justify="right")
        self.e_user.grid(row=1, column=0, pady=5, padx=5)

        ttk.Label(l_f, text="رمز عبور:").grid(row=2, column=1, sticky="e", pady=5, padx=5)
        self.e_pass = ttk.Entry(l_f, show="*", justify="right")
        self.e_pass.grid(row=2, column=0, pady=5, padx=5)

        self.e_pass.bind("<Return>",
                         lambda e: self.auth_controller.handle_admin_login(self.e_user.get(), self.e_pass.get()))
        ttk.Button(l_f, text="ورود به سیستم",
                   command=lambda: self.auth_controller.handle_admin_login(self.e_user.get(), self.e_pass.get())).grid(
            row=3, columnspan=2, pady=20)

    def switch_to_main(self):
        self.f_login.pack_forget()
        self.frame_top_bar = ttk.Frame(self)
        self.frame_top_bar.pack(fill="x", padx=20, pady=10)
        ttk.Label(self.frame_top_bar, text="سامانه مدیریت صندوق", style="Header.TLabel").pack(side="right")
        ttk.Button(self.frame_top_bar, text="خروج", command=self.auth_controller.handle_logout).pack(side="left")

        self.nb = ttk.Notebook(self)
        self.nb.pack(fill="both", expand=True, padx=10, pady=10)

        self.dashboard_tab = DashboardTab(self.nb, self.customers_controller)
        self.customers_tab = CustomersTab(self.nb, self.customers_controller)
        self.register_tab = RegisterTab(self.nb, self.register_controller)
        self.transfer_tab = TransferTab(self.nb, self.transfer_controller)
        self.deposit_tab = DepositWithdrawTab(self.nb, self.deposit_withdraw_controller)

        self.nb.add(self.customers_tab, text=" گزارش‌ها ")
        self.nb.add(self.register_tab, text=" افتتاح حساب ")
        self.nb.add(self.transfer_tab, text=" انتقال وجه ")
        self.nb.add(self.deposit_tab, text=" عملیات مستقیم ")
        self.nb.add(self.dashboard_tab, text=" داشبورد ")
        self.nb.select(self.dashboard_tab)

        # اجرای خودکار رفرش داشبورد و جدولِ گزارش‌ها در لحظه لود شدن و جابجایی بین تب‌ها
        self.nb.bind("<<NotebookTabChanged>>", self._on_tab_change)
        self._on_tab_change()

        self.status = ttk.Label(self, text="آماده عملیات...", foreground="green")
        self.status.pack(side="bottom", fill="x", pady=5)

    def _on_tab_change(self, event=None):
        """متد هوشمند برای آپدیت خودکار تمام داده‌ها هنگام جابجایی تب‌ها"""
        if self.customers_controller:
            self.customers_controller.refresh_dashboard_data()
            if hasattr(self, 'customers_tab'):
                self.customers_controller.handle_customer_search(self.customers_tab.v_q.get())

    def switch_to_login(self):
        self.frame_top_bar.pack_forget()
        self.nb.pack_forget()
        self.status.pack_forget()
        self.e_user.delete(0, tk.END)
        self.e_pass.delete(0, tk.END)
        self.f_login.pack(expand=True, fill="both")

    def update_dashboard_labels(self, stats):
        if hasattr(self, 'dashboard_tab'): self.dashboard_tab.update_data(stats)

    def show_message(self, title, msg, is_error=False):
        if is_error:
            messagebox.showerror(title, msg)
        else:
            if hasattr(self, 'status'): self.status.config(text=f"✅ {msg}")

    def show_persistent_message(self, title, msg):
        messagebox.showinfo(title, msg)

    def ask_save_file(self, ext, init, title, types):
        return filedialog.asksaveasfilename(defaultextension=ext, initialfile=init, title=title, filetypes=types)

    def ask_yes_no(self, title, msg):
        return messagebox.askyesno(title, msg)

    def show_history_window(self, acc, records):
        w = tk.Toplevel(self)
        w.title(f"تاریخچه حساب {acc}")
        w.geometry("850x450")
        txt = tk.Text(w, font=("Samim", 10), padx=12, pady=12, bg="#fbfbfb", fg="#1a1a1a")
        txt.pack(expand=True, fill="both")
        txt.tag_configure("rtl", justify="right")
        txt.tag_configure("d", foreground="#1a7f37", font=("Samim", 10, "bold"))
        txt.tag_configure("w", foreground="#b91c1c", font=("Samim", 10, "bold"))
        txt.tag_configure("t", foreground="#0078d4", font=("Samim", 10, "bold"))

        if not records: txt.insert(tk.END, "تراکنشی یافت نشد.\n")
        for r in records:
            c = "d" if "واریز" in r[0] else "w" if "برداشت" in r[0] else "t"
            txt.insert(tk.END, f"📅 زمان: [{r[3]}] | ")
            txt.insert(tk.END, f"📊 نوع: {r[0]} ", c)
            txt.insert(tk.END, f"| 💵 مبلغ: {int(r[1]):,} | 💰 موجودی: {int(r[2]):,} | 📝 {r[4]}\n")
            txt.insert(tk.END, "-" * 80 + "\n\n")
        txt.tag_add("rtl", "1.0", "end")
        txt.config(state="disabled")

    def start_app(self):
        self.mainloop()