import sqlite3


class Database:
    def __init__(self, path="taxi.db"):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS drivers (
            id INTEGER PRIMARY KEY,
            surname TEXT NOT NULL,
            deduction_pct INTEGER NOT NULL
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS cars (
            car_no TEXT PRIMARY KEY,
            brand TEXT NOT NULL,
            driver_id INTEGER NOT NULL,
            FOREIGN KEY(driver_id) REFERENCES drivers(id)
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS shifts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            driver_id INTEGER,
            car_no TEXT,
            date TEXT,
            start_time TEXT,
            hours INTEGER,
            shift_no INTEGER,
            revenue REAL,
            avg_hour REAL,
            deduction REAL,
            net REAL,
            FOREIGN KEY(driver_id) REFERENCES drivers(id),
            FOREIGN KEY(car_no) REFERENCES cars(car_no)
        )
        """)

        self.conn.commit()

    # DRIVERS
    def add_driver(self, id, surname, pct):
        self.cursor.execute(
            "INSERT OR REPLACE INTO drivers VALUES (?, ?, ?)",
            (id, surname, pct)
        )
        self.conn.commit()

    def get_drivers(self):
        self.cursor.execute("""
            SELECT id, surname, deduction_pct 
            FROM drivers
            ORDER BY surname
        """)
        rows = self.cursor.fetchall()

        return [
            {
                "id": r[0],
                "surname": r[1],
                "percent": r[2]  # ключ percent — бо StatsTab очікує його
            }
            for r in rows
        ]

    # CARS
    def add_car(self, car_no, brand, driver_id):
        self.cursor.execute(
            "INSERT OR REPLACE INTO cars VALUES (?, ?, ?)",
            (car_no, brand, driver_id)
        )
        self.conn.commit()

    def get_cars_by_driver(self, driver_id):
        return [dict(x) for x in self.cursor.execute(
            "SELECT * FROM cars WHERE driver_id=?",
            (driver_id,)
        ).fetchall()]

    def get_all_cars(self):
        return [dict(x) for x in self.cursor.execute("SELECT * FROM cars").fetchall()]

    # SHIFTS
    def add_shift(self, driver_id, car_no, date, start_time, hours, shift_no, revenue,
                  avg_hour, deduction, net):

        self.cursor.execute("""
        INSERT INTO shifts (driver_id, car_no, date, start_time, hours,
                            shift_no, revenue, avg_hour, deduction, net)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (driver_id, car_no, date, start_time, hours, shift_no,
              revenue, avg_hour, deduction, net))

        self.conn.commit()

    def get_all_shifts(self):
        return [dict(x) for x in self.cursor.execute(
            "SELECT * FROM shifts ORDER BY date"
        ).fetchall()]

    def get_shifts(self, driver_id=None):
        if driver_id:
            return [dict(x) for x in self.cursor.execute(
                "SELECT * FROM shifts WHERE driver_id=? ORDER BY date",
                (driver_id,)
            ).fetchall()]
        return self.get_all_shifts()
