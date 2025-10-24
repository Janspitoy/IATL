import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score, mean_squared_error
import matplotlib.pyplot as plt

# Генерація синтетичного датасету (оскільки оригінальний не має глюкози; припускаємо стабілізована глюкоза)
np.random.seed(42)
n_samples = 100
glucose = np.sort(np.random.uniform(70, 180, n_samples))  # Stabilized glucose mg/dL
a_true, b_true, c_true = 10, 0.05, -0.0001
hb_true = a_true + b_true * glucose + c_true * glucose**2
noise = np.random.normal(0, 0.5, n_samples)
hb = hb_true + noise

df = pd.DataFrame({
    'Stabilized_Glucose_mg_dL': glucose,
    'Hemoglobin_g_dL': hb
})
df.to_csv('glucose_hemoglobin_dataset.csv', index=False)

# Визначення нелінійної моделі (квадратична як приклад нелінійної)
def quadratic_model(x, a, b, c):
    return a + b * x + c * x**2

# Оцінювання параметрів за допомогою Nonlinear Least Squares
popt, pcov = curve_fit(quadratic_model, df['Stabilized_Glucose_mg_dL'], df['Hemoglobin_g_dL'], p0=[10, 0.05, -0.0001])

# Прогнозовані значення
hb_pred = quadratic_model(df['Stabilized_Glucose_mg_dL'], *popt)

# Обчислення метрик якості
r2 = r2_score(df['Hemoglobin_g_dL'], hb_pred)
mse = mean_squared_error(df['Hemoglobin_g_dL'], hb_pred)

# Виведення результатів
print("Обчислені параметри нелінійної моделі hb = a + b*x + c*x^2:")
print(f"a = {popt[0]:.4f}")
print(f"b = {popt[1]:.4f}")
print(f"c = {popt[2]:.4f}")

# Візуалізація
plt.scatter(df['Stabilized_Glucose_mg_dL'], df['Hemoglobin_g_dL'], label='Дані')
plt.plot(glucose, hb_pred, color='red', label='Фітована модель')
plt.xlabel('Стабілізована глюкоза (mg/dL)')
plt.ylabel('Гемоглобін (g/dL)')
plt.legend()
plt.show()
