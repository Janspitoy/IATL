import tkinter as tk
from tkinter import ttk

from database import Database
from gui.drivers_tab import DriversTab
from gui.cars_tab import CarsTab
from gui.shifts_tab import ShiftsTab
from gui.stats_tab import StatsTab
from excel_export import ExcelExporter


class TaxiApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Taxi Management System")
        self.geometry("1350x900")
        self.configure(bg="#F1F5F9")

        self.style = ttk.Style()
        self._configure_styles()

        # ----- DB -----
        self.db = Database("taxi.db")
        self.db.create_tables()
        self.exporter = ExcelExporter(self.db)

        # ----- UI -----
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=24, pady=24)

        self.drivers_tab = DriversTab(notebook, self.db, self)
        self.cars_tab = CarsTab(notebook, self.db, self)
        self.shifts_tab = ShiftsTab(notebook, self.db, self)
        self.stats_tab = StatsTab(notebook, self.db, self.exporter)

        notebook.add(self.shifts_tab, text="Зміни")
        notebook.add(self.drivers_tab, text="Водії")
        notebook.add(self.cars_tab, text="Машини")
        notebook.add(self.stats_tab, text="Статистика")

    # -------------------------------------------------
    # MODERN GLOBAL UI STYLE
    # -------------------------------------------------
    def _configure_styles(self):
        s = self.style
        s.theme_use("default")

        PRIMARY = "#2563EB"
        BG = "#F1F5F9"
        CARD = "#FFFFFF"
        BORDER = "#E2E8F0"
        TEXT = "#1E293B"

        # GLOBAL
        s.configure(".", background=BG, foreground=TEXT, font=("Segoe UI", 11))
        s.configure("TFrame", background=BG)
        s.configure("TLabel", background=BG, foreground=TEXT)

        # ENTRY
        s.configure("TEntry",
                    padding=8,
                    fieldbackground=CARD,
                    bordercolor=BORDER,
                    relief="flat")

        # COMBOBOX
        s.configure("TCombobox",
                    padding=8,
                    fieldbackground=CARD,
                    bordercolor=BORDER,
                    relief="flat")

        # BUTTON
        s.configure("TButton",
                    padding=(14, 8),
                    foreground="white",
                    background=PRIMARY,
                    relief="flat",
                    font=("Segoe UI Semibold", 11))
        s.map("TButton",
              background=[("active", "#1E4FCF")])

        # NOTEBOOK
        s.configure("TNotebook", background=BG, borderwidth=0)
        s.configure("TNotebook.Tab", background="#E2E8F0", padding=[20, 10])
        s.map("TNotebook.Tab",
              background=[("selected", CARD)],
              foreground=[("selected", TEXT)])

        # TREEVIEW
        s.configure("Treeview",
                    font=("Segoe UI", 10),
                    background=CARD,
                    fieldbackground=CARD,
                    rowheight=30)
        s.configure("Treeview.Heading",
                    font=("Segoe UI Semibold", 11),
                    background="#E2E8F0")

        # CUSTOM CARD FRAME
        s.configure("Card.TFrame",
                    background=CARD,
                    relief="flat")

    def refresh_all(self):
        self.drivers_tab.load()
        self.cars_tab.load()
        self.shifts_tab.load()
        self.stats_tab.refresh()


if __name__ == "__main__":
    app = TaxiApp()
    app.mainloop()
