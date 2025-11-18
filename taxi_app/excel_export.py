import pandas as pd
from datetime import datetime
import os


class ExcelExporter:
    def __init__(self, db, out_dir="."):
        self.db = db
        self.out_dir = out_dir

    def export_all(self):
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(self.out_dir, f"taxi_full_report_{now}.xlsx")

        drivers = self.db.get_drivers() or []

        # Якщо немає водіїв — створимо простий summary лист, щоб openpyxl не впав
        if not drivers:
            with pd.ExcelWriter(path, engine="openpyxl") as writer:
                pd.DataFrame([["No drivers found"]]).to_excel(writer, sheet_name="summary", index=False, header=False)
            return path

        with pd.ExcelWriter(path, engine="openpyxl") as writer:
            for d in drivers:
                # Безпечне читання поля відсотка (підтримка декількох варіантів імен)
                deduction_pct = d.get("deduction_pct", d.get("percent", d.get("pct", "")))
                # shifts для цього водія
                shifts = []
                try:
                    shifts = self.db.get_shifts(driver_id=d.get("id"))
                except Exception:
                    # якщо get_shifts не існує, пробуємо get_all_shifts і фільтруємо
                    try:
                        all_shifts = self.db.get_all_shifts()
                        shifts = [s for s in all_shifts if s.get("driver_id") == d.get("id")]
                    except Exception:
                        shifts = []

                # Метадані (рядки)
                meta = pd.DataFrame([
                    ["Дата створення", datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                    ["Відсоток відрахувань", f"{deduction_pct}"],
                    ["Прізвище водія", d.get("surname", "")],
                    ["", ""]
                ])

                # DataFrame зі змінами (може бути порожнім)
                df = pd.DataFrame(shifts) if shifts else pd.DataFrame()

                if not df.empty:
                    # перейменування колонок на українські (ті, що є)
                    rename_map = {
                        "car_no": "Номер машини",
                        "brand": "Марка",
                        "date": "Дата",
                        "start_time": "Час початку",
                        "hours": "Тривалість",
                        "shift_no": "Зміна",
                        "revenue": "Виторг",
                        "avg_hour": "Середньогодинний виторг",
                        "deduction": "Відрахування",
                        "net": "Залишок"
                    }
                    # Перейменовуємо тільки ті колонки, які реально присутні
                    rename_map = {k: v for k, v in rename_map.items() if k in df.columns}
                    df = df.rename(columns=rename_map)

                # Запис мета та таблиці (якщо таблиця є, то з відступом startrow=4)
                sheet_name = str(d.get("id", "unknown"))
                # Безпечне ім'я листа — truncate до 31 символу (Excel обмеження)
                if len(sheet_name) > 31:
                    sheet_name = sheet_name[:31]

                meta.to_excel(writer, sheet_name=sheet_name, index=False, header=False)
                if not df.empty:
                    df.to_excel(writer, sheet_name=sheet_name, startrow=4, index=False)

                # Pivot per shift: для кожної з 1,2,3 створюємо окремий лист із сумами по датах і машинах
                for shift_no in [1, 2, 3]:
                    s = [x for x in shifts if x.get("shift_no") == shift_no]
                    if s:
                        pivot = pd.pivot_table(
                            pd.DataFrame(s),
                            index="date",
                            columns="car_no",
                            values="revenue",
                            aggfunc="sum",
                            fill_value=0
                        )
                        pivot_sheet = f"{d.get('id')}_shift{shift_no}"
                        if len(pivot_sheet) > 31:
                            pivot_sheet = pivot_sheet[:31]
                        pivot.to_excel(writer, sheet_name=pivot_sheet)

        return path
