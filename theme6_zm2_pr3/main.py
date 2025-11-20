import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# 1. Завантаження даних

df = pd.read_csv("olap_variant7_dataset_1000.csv", parse_dates=["AssignDate"])

# 2. Створення вимірів (Dimension Tables)

# DIM Clients
dim_clients = (
    df[["Client_LastName", "Client_City", "Client_Country"]]
    .drop_duplicates()
    .reset_index(drop=True)
)
dim_clients.insert(0, "ClientID", range(1, len(dim_clients) + 1))

# DIM Suppliers
dim_suppliers = (
    df[["Supplier_Name", "Supplier_City", "Supplier_Country"]]
    .drop_duplicates()
    .reset_index(drop=True)
)
dim_suppliers.insert(0, "SupplierID", range(1, len(dim_suppliers) + 1))

# DIM Products
dim_products = (
    df[["Brand", "Category"]]
    .drop_duplicates()
    .reset_index(drop=True)
)
dim_products.insert(0, "ProductID", range(1, len(dim_products) + 1))

# DIM Dates
dates = pd.DataFrame({
    "AssignDate": pd.date_range(df["AssignDate"].min(), df["AssignDate"].max())
})
dates["Day"] = dates["AssignDate"].dt.day
dates["Month"] = dates["AssignDate"].dt.month
dates["MonthName"] = dates["AssignDate"].dt.month_name()
dates["Year"] = dates["AssignDate"].dt.year
dates["Weekday"] = dates["AssignDate"].dt.day_name()
dates.insert(0, "DateID", range(1, len(dates) + 1))

# 3. Створення Факт-таблиці (Fact Table)

fact = (
    df.merge(dim_clients, on=["Client_LastName", "Client_City", "Client_Country"])
      .merge(dim_suppliers, on=["Supplier_Name", "Supplier_City", "Supplier_Country"])
      .merge(dim_products, on=["Brand", "Category"])
      .merge(dates[["AssignDate", "DateID"]], on="AssignDate")
)

fact_table = fact[[
    "AssignDate", "DateID",
    "ClientID", "SupplierID", "ProductID",
    "Quantity", "Price"
]].copy()

fact_table.insert(0, "FactID", range(1, len(fact_table) + 1))

# 4. Pivot-таблиця (OLAP-зріз)

merged = (
    fact_table
    .merge(dim_clients, on="ClientID")
    .merge(dim_suppliers, on="SupplierID")
    .merge(dim_products, on="ProductID")
)

pivot = pd.pivot_table(
    merged,
    values=["Price", "Quantity"],
    index=["AssignDate", "Client_LastName", "Client_City", "Client_Country"],
    columns=["Supplier_Name", "Brand", "Category"],
    aggfunc={"Price": "mean", "Quantity": "sum"},
    fill_value=0
)

# 5. Збереження структури (всі CSV + Excel з pivot)

out = Path("olap_variant7_star_schema")
out.mkdir(exist_ok=True)

dim_clients.to_csv(out / "dim_clients.csv", index=False)
dim_suppliers.to_csv(out / "dim_suppliers.csv", index=False)
dim_products.to_csv(out / "dim_products.csv", index=False)
dates.to_csv(out / "dim_dates.csv", index=False)
fact_table.to_csv(out / "fact_orders.csv", index=False)

with pd.ExcelWriter(out / "pivot_variant7.xlsx") as writer:
    df.to_excel(writer, sheet_name="raw", index=False)
    dim_clients.to_excel(writer, sheet_name="dim_clients", index=False)
    dim_suppliers.to_excel(writer, sheet_name="dim_suppliers", index=False)
    dim_products.to_excel(writer, sheet_name="dim_products", index=False)
    dates.to_excel(writer, sheet_name="dim_dates", index=False)
    fact_table.to_excel(writer, sheet_name="fact", index=False)
    pivot_flat = pivot.copy()
    pivot_flat.columns = [
        f"{val1} | {val2} | {val3} | {val4}"
        for (val1, val2, val3, val4) in pivot_flat.columns
    ]
    pivot_flat = pivot_flat.reset_index()
    pivot_flat.to_excel(writer, sheet_name="pivot", index=False)

# 6. Діаграми

# 6.1 — к-сть замовлень по датах
qty_by_date = fact_table.groupby("AssignDate")["Quantity"].sum()
plt.figure(figsize=(10, 4))
plt.plot(qty_by_date.index, qty_by_date.values)
plt.title("Quantity by AssignDate")
plt.xlabel("Date")
plt.ylabel("Total Quantity")
plt.tight_layout()
plt.savefig(out / "chart_quantity_by_date.png")
plt.close()

# 6.2 — середня ціна по бренду
avg_price_brand = merged.groupby("Brand")["Price"].mean().sort_values()
plt.figure(figsize=(8, 4))
plt.bar(avg_price_brand.index, avg_price_brand.values)
plt.title("Average Price by Brand")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(out / "chart_price_by_brand.png")
plt.close()

# 6.3 — к-сть по постачальнику
qty_supplier = merged.groupby("Supplier_Name")["Quantity"].sum()
plt.figure(figsize=(6, 4))
plt.bar(qty_supplier.index, qty_supplier.values)
plt.title("Quantity by Supplier")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(out / "chart_quantity_by_supplier.png")
plt.close()

