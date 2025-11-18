# gui/shifts_tab.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class ShiftsTab(ttk.Frame):
    def __init__(self, parent, db, app):
        super().__init__(parent)
        self.db = db
        self.app = app
        self._build()

    def _build(self):
        # CARD
        card = ttk.Frame(self, style="Card.TFrame")
        card.pack(fill="x", padx=20, pady=20, ipadx=20, ipady=20)

        ttk.Label(card, text="Створення зміни", font=("Segoe UI Semibold", 16)).grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 20)
        )

        # DRIVER
        ttk.Label(card, text="Водій:").grid(row=1, column=0, sticky="w", pady=8)
        self.driver_var = tk.StringVar()
        self.driver_combo = ttk.Combobox(card, textvariable=self.driver_var, state="readonly", width=40)
        self.driver_combo.grid(row=1, column=1, sticky="w", pady=8)
        self.driver_combo.bind("<<ComboboxSelected>>", self.load_cars)

        # CAR
        ttk.Label(card, text="Машина:").grid(row=2, column=0, sticky="w", pady=8)
        self.car_var = tk.StringVar()
        self.car_combo = ttk.Combobox(card, textvariable=self.car_var, state="readonly", width=40)
        self.car_combo.grid(row=2, column=1, sticky="w", pady=8)

        # DATE
        ttk.Label(card, text="Дата (YYYY-MM-DD):").grid(row=3, column=0, sticky="w", pady=8)
        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        ttk.Entry(card, textvariable=self.date_var, width=40).grid(row=3, column=1, sticky="w", pady=8)

        # START TIME
        ttk.Label(card, text="Час початку (0–23):").grid(row=4, column=0, sticky="w", pady=8)
        self.time_var = tk.StringVar()
        ttk.Entry(card, textvariable=self.time_var, width=40).grid(row=4, column=1, sticky="w", pady=8)

        # HOURS
        ttk.Label(card, text="Тривалість (години):").grid(row=5, column=0, sticky="w", pady=8)
        self.hours_var = tk.StringVar()
        ttk.Entry(card, textvariable=self.hours_var, width=40).grid(row=5, column=1, sticky="w", pady=8)

        # REVENUE
        ttk.Label(card, text="Виторг:").grid(row=6, column=0, sticky="w", pady=8)
        self.revenue_var = tk.StringVar()
        ttk.Entry(card, textvariable=self.revenue_var, width=40).grid(row=6, column=1, sticky="w", pady=8)

        ttk.Button(card, text="Створити зміну", command=self.add_shift).grid(
            row=7, column=1, sticky="e", pady=16
        )

        # TABLE
        self.table = ttk.Treeview(
            self,
            columns=("id", "driver_id", "car_no", "date", "shift_no", "hours", "revenue"),
            show="headings",
            height=16,
        )
        for col in self.table["columns"]:
            self.table.heading(col, text=col)
            self.table.column(col, width=140)
        self.table.pack(fill="both", expand=True, padx=20, pady=12)

        self.load()

    def load_cars(self, _=None):
        # use get_cars_by_driver (exists in database.py)
        drv_txt = self.driver_var.get().strip()
        try:
            driver_id = int(drv_txt.split(" ")[0])
        except Exception:
            self.car_combo["values"] = []
            return

        cars = self.db.get_cars_by_driver(driver_id)
        self.car_combo["values"] = [c.get("car_no") for c in cars]

    def add_shift(self):
        drv_txt = self.driver_var.get().strip()
        try:
            driver_id = int(drv_txt.split(" ")[0])
        except Exception:
            messagebox.showwarning("Помилка", "Оберіть водія.")
            return

        car_no = self.car_var.get().strip()
        date = self.date_var.get().strip()
        if not date:
            messagebox.showwarning("Помилка", "Введіть дату.")
            return

        try:
            start = int(self.time_var.get())
        except Exception:
            messagebox.showwarning("Помилка", "Час початку має бути цілим (0–23).")
            return

        try:
            hours = float(self.hours_var.get())
            if hours <= 0:
                raise ValueError()
        except Exception:
            messagebox.showwarning("Помилка", "Тривалість має бути додатнім числом.")
            return

        try:
            revenue = float(self.revenue_var.get())
        except Exception:
            messagebox.showwarning("Помилка", "Виторг має бути числом.")
            return

        # AUTO SHIFT NUMBER
        if 6 <= start < 12:
            shift_no = 1
        elif 12 <= start < 18:
            shift_no = 2
        else:
            shift_no = 3

        # get driver deduction percent from db.get_drivers()
        driver = None
        for d in self.db.get_drivers():
            if d.get("id") == driver_id:
                driver = d
                break

        if driver is None:
            messagebox.showerror("Помилка", "Не знайдено водія в базі.")
            return

        pct = driver.get("deduction_pct", 0)

        avg_hour = revenue / hours if hours != 0 else 0
        deduction = revenue * (pct / 100.0)
        net = revenue - deduction

        try:
            self.db.add_shift(driver_id, car_no, date, start, hours,
                              shift_no, revenue, avg_hour, deduction, net)
        except Exception as e:
            messagebox.showerror("Помилка БД", str(e))
            return

        # clear inputs
        self.time_var.set("")
        self.hours_var.set("")
        self.revenue_var.set("")

        self.load()
        self.app.refresh_all()

    def load(self):
        # populate drivers
        drivers = self.db.get_drivers()
        self.driver_combo["values"] = [f"{d.get('id')} {d.get('surname')}" for d in drivers]

        # table
        for r in self.table.get_children():
            self.table.delete(r)

        for s in self.db.get_all_shifts():
            self.table.insert("", "end", values=(
                s.get("id"), s.get("driver_id"), s.get("car_no"),
                s.get("date"), s.get("shift_no"), s.get("hours"), s.get("revenue")
            ))
