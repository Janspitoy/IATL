# gui/stats_tab.py
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# optional calendar widget
try:
    from tkcalendar import Calendar
except Exception:
    Calendar = None


class StatsTab(ttk.Frame):
    def __init__(self, parent, db, exporter):
        super().__init__(parent)
        self.db = db
        self.exporter = exporter
        self._build()

    def _build(self):
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        # LEFT FILTER SIDEBAR
        card = ttk.Frame(container, style="Card.TFrame")
        card.pack(side="left", fill="y", padx=(0, 20), pady=10, ipadx=20, ipady=20)

        ttk.Label(card, text="Фільтри статистики", font=("Segoe UI Semibold", 15)).pack(anchor="w")

        # DRIVERS
        ttk.Label(card, text="Водії:").pack(anchor="w", pady=(12, 6))
        self.driver_listbox = tk.Listbox(card, selectmode=tk.MULTIPLE, height=6)
        self.driver_listbox.pack(fill="x", pady=6)
        self._load_drivers()

        # PERIOD
        ttk.Label(card, text="Період:").pack(anchor="w", pady=(12, 6))
        self.period_var = tk.StringVar()
        self.period = ttk.Combobox(
            card,
            textvariable=self.period_var,
            state="readonly",
            values=[
                "Сьогодні",
                "Вчора",
                "7 днів",
                "30 днів",
                "Місяць",
                "Рік",
                "Весь час",
            ],
        )
        self.period.current(2)
        self.period.pack(fill="x", pady=6)

        # SPECIFIC DATE + CALENDAR BUTTON
        ttk.Label(card, text="Конкретна дата (опц.):").pack(anchor="w", pady=(12, 6))
        date_row = ttk.Frame(card)
        date_row.pack(fill="x", pady=6)
        self.specific_date_var = tk.StringVar()
        self.specific_entry = ttk.Entry(date_row, textvariable=self.specific_date_var)
        self.specific_entry.pack(side="left", fill="x", expand=True)
        self.cal_button = ttk.Button(date_row, text="Вибрати...", width=12, command=self.open_calendar)
        self.cal_button.pack(side="left", padx=(8, 0))

        # ACTIONS
        ttk.Button(card, text="Оновити", command=self.refresh).pack(fill="x", pady=(16, 6))
        ttk.Button(card, text="Експорт у Excel", command=self.export).pack(fill="x")

        # RIGHT SIDE: TABLE + CHART
        right = ttk.Frame(container)
        right.pack(fill="both", expand=True)

        # TABLE
        self.table = ttk.Treeview(
            right,
            columns=("date", "driver", "car", "shift", "rev", "ded", "net"),
            show="headings",
            height=14,
        )
        for col in self.table["columns"]:
            self.table.heading(col, text=col)
            self.table.column(col, width=130, anchor="center")
        self.table.pack(fill="x", pady=12)

        # CHART
        self.fig, self.ax = plt.subplots(figsize=(10, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=right)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # initial refresh
        self.refresh()

    # -----------------------------
    # Drivers
    # -----------------------------
    def _load_drivers(self):
        self.driver_list = self.db.get_drivers()
        self.driver_listbox.delete(0, tk.END)
        for d in self.driver_list:
            self.driver_listbox.insert(tk.END, f"{d.get('id')} — {d.get('surname')}")

    def _selected_drivers(self):
        sel = self.driver_listbox.curselection()
        if not sel:
            return []
        return [self.driver_list[i]["id"] for i in sel]

    # -----------------------------
    # Calendar
    # -----------------------------
    def open_calendar(self):
        if Calendar is None:
            messagebox.showinfo(
                "tkcalendar не встановлено",
                "Встановіть tkcalendar, щоб використовувати календар:\n\npip install tkcalendar",
            )
            return

        # Toplevel with calendar
        top = tk.Toplevel(self)
        top.title("Вибір дати")
        cal = Calendar(top, selectmode="day", date_pattern="yyyy-mm-dd")
        cal.pack(padx=10, pady=10)

        def on_pick():
            self.specific_date_var.set(cal.get_date())
            top.destroy()

        ttk.Button(top, text="OK", command=on_pick).pack(pady=(0, 10))

    # -----------------------------
    # Export
    # -----------------------------
    def export(self):
        path = self.exporter.export_all()
        messagebox.showinfo("Експорт", f"Файл створено:\n{path}")

    # -----------------------------
    # Refresh
    # -----------------------------
    def refresh(self):
        shifts = self.db.get_all_shifts()
        if not shifts:
            self._clear_visuals()
            return

        # create dataframe, robust date parsing
        df = pd.DataFrame(shifts)
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"], errors="coerce")
        else:
            df["date"] = pd.NaT

        # ensure start_time exists (for hour grouping)
        if "start_time" not in df.columns:
            df["start_time"] = pd.NA

        # Filter by drivers
        selected = self._selected_drivers()
        if selected:
            df = df[df["driver_id"].isin(selected)]

        # Specific date filter (overrides period aggregation for plotting mode)
        specific_date = self.specific_date_var.get().strip()
        if specific_date:
            try:
                sd = datetime.strptime(specific_date, "%Y-%m-%d").date()
                df = df[df["date"].dt.date == sd]
            except Exception:
                messagebox.showwarning("Помилка", "Невірний формат дати (має бути YYYY-MM-DD).")
                return

        # Period filter (applied after specific-date filter; specific date already narrowed)
        df = self._apply_period_filter(df)

        # Normalize: drop rows with invalid dates (keep for table if needed)
        # For plotting we need valid dates; for table we will format safely
        self._load_table(df)

        # Chart
        self._load_chart(df)

    # -----------------------------
    # Period filter
    # -----------------------------
    def _apply_period_filter(self, df):
        if df.empty:
            return df

        # if specific date was set -> do not further narrow by period (we already applied)
        # but keep behavior consistent: if no specific date, apply period
        if self.specific_date_var.get().strip():
            return df

        today = datetime.now().date()
        period = self.period_var.get()

        if period == "Сьогодні":
            return df[df["date"].dt.date == today]

        if period == "Вчора":
            return df[df["date"].dt.date == today - timedelta(days=1)]

        if period == "7 днів":
            return df[df["date"] >= pd.to_datetime(today - timedelta(days=6))]

        if period == "30 днів":
            return df[df["date"] >= pd.to_datetime(today - timedelta(days=29))]

        if period == "Місяць":
            first_day = today.replace(day=1)
            return df[df["date"] >= pd.to_datetime(first_day)]

        if period == "Рік":
            year_ago = today.replace(year=today.year - 1)
            return df[df["date"] >= pd.to_datetime(year_ago)]

        return df  # "Весь час"

    # -----------------------------
    # Table
    # -----------------------------
    def _load_table(self, df):
        # clear
        for r in self.table.get_children():
            self.table.delete(r)

        # show rows; format date safely
        for _, s in df.iterrows():
            date_val = ""
            try:
                if not pd.isna(s.get("date")):
                    date_val = pd.to_datetime(s.get("date")).strftime("%Y-%m-%d")
            except Exception:
                date_val = str(s.get("date", ""))

            self.table.insert("", "end", values=(
                date_val,
                s.get("driver_id", ""),
                s.get("car_no", ""),
                s.get("shift_no", ""),
                s.get("revenue", ""),
                s.get("deduction", ""),
                s.get("net", ""),
            ))

    # -----------------------------
    # Chart
    # -----------------------------
    def _load_chart(self, df):
        self.ax.clear()

        if df.empty:
            self.canvas.draw()
            return

        # determine mode
        specific_date = self.specific_date_var.get().strip()
        if specific_date:
            mode = "hour"
        else:
            period = self.period_var.get()
            mode = "month" if period == "Рік" else "day"

        # Prepare total series and per-driver series
        try:
            if mode == "hour":
                # use start_time (assumed integer 0-23)
                df_hours = df.copy()
                df_hours["hour"] = df_hours["start_time"].astype("Int64")
                total = df_hours.groupby("hour")["revenue"].sum().sort_index()
                x_total = list(total.index)
                y_total = list(total.values)
                self.ax.plot(x_total, y_total, label="Загальний виторг", marker="o", linewidth=2)
                # per driver
                drivers = {d["id"]: d["surname"] for d in self.db.get_drivers()}
                for did in df_hours["driver_id"].unique():
                    sub = df_hours[df_hours["driver_id"] == did]
                    sgroup = sub.groupby("hour")["revenue"].sum().sort_index()
                    self.ax.plot(list(sgroup.index), list(sgroup.values), linestyle="--", marker="o",
                                 label=f"{did} — {drivers.get(did, '?')}")
                self.ax.set_xlabel("Година")
                self.ax.set_ylabel("Виторг")
                self.ax.set_title("Виторг по годинах")
                self.ax.set_xticks(sorted(set(x_total)))
            elif mode == "month":
                dfm = df.copy()
                dfm["month"] = dfm["date"].dt.to_period("M")
                total = dfm.groupby("month")["revenue"].sum().sort_index()
                x_total = total.index.astype(str)
                y_total = total.values
                self.ax.plot(x_total, y_total, label="Загальний виторг", marker="o", linewidth=2)
                drivers = {d["id"]: d["surname"] for d in self.db.get_drivers()}
                for did in dfm["driver_id"].unique():
                    sub = dfm[dfm["driver_id"] == did]
                    sgroup = sub.groupby("month")["revenue"].sum().sort_index()
                    self.ax.plot(sgroup.index.astype(str), sgroup.values, linestyle="--", marker="o",
                                 label=f"{did} — {drivers.get(did, '?')}")
                self.ax.set_xlabel("Місяць")
                self.ax.set_ylabel("Виторг")
                self.ax.set_title("Виторг по місяцях")
            else:  # day
                dfd = df.copy()
                dfd["day"] = dfd["date"].dt.date
                total = dfd.groupby("day")["revenue"].sum().sort_index()
                x_total = [d.strftime("%Y-%m-%d") for d in total.index]
                y_total = total.values
                self.ax.plot(x_total, y_total, label="Загальний виторг", marker="o", linewidth=2)
                drivers = {d["id"]: d["surname"] for d in self.db.get_drivers()}
                for did in dfd["driver_id"].unique():
                    sub = dfd[dfd["driver_id"] == did]
                    sgroup = sub.groupby(sub["date"].dt.date)["revenue"].sum().sort_index()
                    x = [d.strftime("%Y-%m-%d") for d in sgroup.index]
                    self.ax.plot(x, sgroup.values, linestyle="--", marker="o",
                                 label=f"{did} — {drivers.get(did, '?')}")
                self.ax.set_xlabel("Дата")
                self.ax.set_ylabel("Виторг")
                self.ax.set_title("Виторг по днях")

            self.ax.legend()
            self.ax.tick_params(axis="x", rotation=45)
        except Exception as e:
            # if something unexpected happens, show a message and draw whatever possible
            messagebox.showwarning("Помилка побудови графіка", f"Сталася помилка при побудові графіка:\n{e}")

        self.canvas.draw()

    # -----------------------------
    def _clear_visuals(self):
        for r in self.table.get_children():
            self.table.delete(r)
        self.ax.clear()
        self.canvas.draw()
