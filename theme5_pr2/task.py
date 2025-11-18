import pandas as pd

sales = pd.DataFrame({
    "promotion_id": [1, 1, 2, 2, 3],
    "store_sales": [120, 90, 100, 80, 150],
    "store_cost": [70, 55, 60, 40, 90],
    "unit_sales": [10, 8, 9, 7, 14]
})

promotion = pd.DataFrame({
    "promotion_id": [1, 2, 3],
    "media_type": ["In-Store Coupon", "Radio", "In-Store Coupon"],
    "end_date": ["2012-01-18", "2012-01-18", "2012-02-01"]
})

promotion["end_date"] = pd.to_datetime(promotion["end_date"])

cube = sales.merge(promotion, on="promotion_id")
print(cube)

hierarchy = cube.groupby(
    ["end_date", "media_type"]
).agg({
    "store_sales": "sum",
    "store_cost": "sum",
    "unit_sales": "sum"
}).reset_index()

print(hierarchy)

slice_var7 = cube[
    (cube["end_date"] == "2012-01-18") &
    (cube["media_type"] == "In-Store Coupon")
]

print(slice_var7)

drill_up = cube.groupby("end_date")["store_sales"].sum()
print(drill_up)

drill_down = cube.groupby(["end_date", "media_type"])["store_sales"].sum()
print(drill_down)
