# gui/cars_tab.py
import tkinter as tk
from tkinter import ttk, messagebox


class CarsTab(ttk.Frame):
    def __init__(self, parent, db, app):
        super().__init__(parent)
        self.db = db
        self.app = app
        self._build()

    def _build(self):
        # CARD
        card = ttk.Frame(self, style="Card.TFrame")
        card.pack(fill="x", padx=20, pady=20, ipadx=20, ipady=20)

        ttk.Label(card, text="Додавання машини", font=("Segoe UI Semibold", 16)).grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 20)
        )

        # DRIVER
        ttk.Label(card, text="Водій:").grid(row=1, column=0, sticky="w", pady=8)
        self.driver_var = tk.StringVar()
        self.driver_combo = ttk.Combobox(card, textvariable=self.driver_var, state="readonly", width=40)
        self.driver_combo.grid(row=1, column=1, sticky="w", pady=8)

        # CAR NO
        ttk.Label(card, text="Номер авто:").grid(row=2, column=0, sticky="w", pady=8)
        self.car_no_var = tk.StringVar()
        ttk.Entry(card, textvariable=self.car_no_var, width=40).grid(row=2, column=1, sticky="w", pady=8)

        # BRAND
        ttk.Label(card, text="Марка авто:").grid(row=3, column=0, sticky="w", pady=8)
        self.brand_var = tk.StringVar()
        ttk.Entry(card, textvariable=self.brand_var, width=40).grid(row=3, column=1, sticky="w", pady=8)

        ttk.Button(card, text="Додати авто", command=self.add_car).grid(
            row=4, column=1, sticky="e", pady=16
        )

        # TABLE
        self.table = ttk.Treeview(
            self,
            columns=("car_no", "brand", "driver_id"),
            show="headings",
            height=16,
        )
        for col in self.table["columns"]:
            self.table.heading(col, text=col)
            self.table.column(col, width=200)
        self.table.pack(fill="both", expand=True, padx=20, pady=12)

        self.load()

    def add_car(self):
        drv_txt = self.driver_var.get().strip()
        try:
            driver_id = int(drv_txt.split(" ")[0])
        except Exception:
            messagebox.showwarning("Помилка", "Оберіть водія зі списку.")
            return

        car_no = self.car_no_var.get().strip()
        brand = self.brand_var.get().strip()

        if not car_no:
            messagebox.showwarning("Помилка", "Введіть номер авто.")
            return
        if not brand:
            messagebox.showwarning("Помилка", "Введіть марку авто.")
            return

        try:
            # note: your database.add_car signature is (car_no, brand, driver_id)
            self.db.add_car(car_no, brand, driver_id)
        except Exception as e:
            messagebox.showerror("Помилка БД", str(e))
            return

        self.car_no_var.set("")
        self.brand_var.set("")
        self.load()
        self.app.refresh_all()

    def load(self):
        # Update driver list
        drivers = self.db.get_drivers()
        self.driver_combo["values"] = [f"{d.get('id','')} {d.get('surname','')}" for d in drivers]

        # Table
        for r in self.table.get_children():
            self.table.delete(r)

        # database has get_all_cars(), use it
        cars = []
        try:
            cars = self.db.get_all_cars()
        except Exception:
            # fallback if someone used different method name
            if hasattr(self.db, "get_cars"):
                cars = self.db.get_cars()
        for c in cars:
            self.table.insert("", "end", values=(c.get("car_no"), c.get("brand"), c.get("driver_id")))
