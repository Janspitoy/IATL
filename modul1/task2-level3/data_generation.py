import numpy as np
import pandas as pd

np.random.seed(42)
n_samples = 100

# Генерація даних
hdl = np.random.normal(60, 10, n_samples)
hdl = np.clip(hdl, 40, 80)

ldl = np.random.normal(100, 20, n_samples)
ldl = np.clip(ldl, 50, 150)

hb_base = np.random.normal(15, 1.5, n_samples)
hb = hb_base + 0.1 * (hdl - 60)  # Позитивна кореляція з HDL
hb = np.clip(hb, 12, 18)

df = pd.DataFrame({
    'HDL_mg_dL': hdl,
    'LDL_mg_dL': ldl,
    'Hemoglobin_g_dL': hb
})

# Збереження
df.to_csv('lipoproteins_hemoglobin_dataset.csv', index=False)
print(df.head(10))