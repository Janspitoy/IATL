# gui/drivers_tab.py
import tkinter as tk
from tkinter import ttk, messagebox


class DriversTab(ttk.Frame):
    def __init__(self, parent, db, app):
        super().__init__(parent)
        self.db = db
        self.app = app
        self._build()

    def _build(self):
        # CARD UI
        card = ttk.Frame(self, style="Card.TFrame")
        card.pack(fill="x", padx=20, pady=20, ipadx=20, ipady=20)

        ttk.Label(card, text="Додавання водія", font=("Segoe UI Semibold", 16)).grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 20)
        )

        # SURNAME
        ttk.Label(card, text="Прізвище:").grid(row=1, column=0, sticky="w", pady=8)
        self.surname_var = tk.StringVar()
        ttk.Entry(card, textvariable=self.surname_var, width=40).grid(
            row=1, column=1, sticky="w", pady=8
        )

        # PERCENT
        ttk.Label(card, text="Відсоток відрахувань:").grid(row=2, column=0, sticky="w", pady=8)
        self.percent_var = tk.StringVar()
        ttk.Entry(card, textvariable=self.percent_var, width=40).grid(
            row=2, column=1, sticky="w", pady=8
        )

        # BUTTON
        ttk.Button(card, text="Додати водія", command=self.add_driver).grid(
            row=3, column=1, sticky="e", pady=16
        )

        # TABLE
        self.table = ttk.Treeview(
            self,
            columns=("id", "surname", "deduction_pct"),
            show="headings",
            height=16,
        )
        for col in self.table["columns"]:
            self.table.heading(col, text=col)
            self.table.column(col, width=180)
        self.table.pack(fill="both", expand=True, padx=20, pady=12)

        self.load()

    def add_driver(self):
        surname = self.surname_var.get().strip()
        pct = self.percent_var.get().strip()

        if not surname:
            messagebox.showwarning("Помилка", "Введіть прізвище водія.")
            return
        if not pct.isdigit():
            messagebox.showwarning("Помилка", "Відсоток має бути цілим числом (без %).")
            return

        # database.add_driver expects (id, surname, pct) according to your database.py
        # Передаємо None як id, щоб SQLite сам присвоїв ключ (INSERT OR REPLACE дозволяє NULL -> автоген).
        try:
            self.db.add_driver(None, surname, int(pct))
        except Exception as e:
            messagebox.showerror("Помилка БД", str(e))
            return

        self.surname_var.set("")
        self.percent_var.set("")
        self.load()
        self.app.refresh_all()

    def load(self):
        for r in self.table.get_children():
            self.table.delete(r)

        drivers = self.db.get_drivers()
        for d in drivers:
            # чорновий захист: якщо поля інші — використовуємо get
            pid = d.get("id", "")
            surname = d.get("surname", "")
            pct = d.get("deduction_pct", d.get("percentage", d.get("pct", "")))
            self.table.insert("", "end", values=(pid, surname, pct))
