import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D # <-- Додано імпорт для 3D

# --- 1. Генерація даних ---
np.random.seed(42)
n_samples = 100

hdl = np.random.normal(60, 10, n_samples)
hdl = np.clip(hdl, 40, 80)

ldl = np.random.normal(100, 20, n_samples)
ldl = np.clip(ldl, 50, 150)

hb_base = np.random.normal(15, 1.5, n_samples)
hb = hb_base + 0.1 * (hdl - 60)
hb = np.clip(hb, 12, 18)

df = pd.DataFrame({
    'HDL_mg_dL': hdl,
    'LDL_mg_dL': ldl,
    'Hemoglobin_g_dL': hb
})

# --- 2. Побудова регресійної моделі ---
X = df[['HDL_mg_dL', 'LDL_mg_dL']]
y = df['Hemoglobin_g_dL']
X_with_const = sm.add_constant(X) # Додаємо константу (intercept)
model = sm.OLS(y, X_with_const).fit()

# --- 3. Виведення результатів (для твого аналізу) ---

# 3.1. Виведення математичного рівняння
print("="*60)
print("Функція регресії (Математичне рівняння)")
print("="*60)
const = model.params['const']
coef_hdl = model.params['HDL_mg_dL']
coef_ldl = model.params['LDL_mg_dL']
print(f"Гемоглобін = {const:.4f} + ({coef_hdl:.4f} * HDL) + ({coef_ldl:.4f} * LDL)")
print("\n")

# 3.2. Виведення повної таблиці OLS
print("="*60)
print("Повна зведена таблиця моделі (OLS Summary)")
print("="*60)
print(model.summary())

# === 4. Візуалізація (Додано) ===
print("\n" + "="*60)
print("Створення 3D візуалізації...")
print("="*60)

# Створення даних для площини регресії
# Нам потрібна сітка значень HDL та LDL, щоб побудувати поверхню
x_surf = np.linspace(df['HDL_mg_dL'].min(), df['HDL_mg_dL'].max(), 20)
y_surf = np.linspace(df['LDL_mg_dL'].min(), df['LDL_mg_dL'].max(), 20)

# np.meshgrid створює матриці координат
x_surf, y_surf = np.meshgrid(x_surf, y_surf)

# Обчислюємо Z (Гемоглобін) для кожної точки на сітці,
# використовуючи коефіцієнти нашої моделі
z_surf = const + (coef_hdl * x_surf) + (coef_ldl * y_surf)

# Створення 3D-графіка
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# 1. Малюємо "хмару" фактичних даних
ax.scatter(df['HDL_mg_dL'], df['LDL_mg_dL'], df['Hemoglobin_g_dL'], c='blue', marker='o', label='Фактичні дані', alpha=0.7)

# 2. Малюємо площину регресії
# 'cmap' - це колірна карта, 'alpha' - прозорість
ax.plot_surface(x_surf, y_surf, z_surf, cmap='viridis', alpha=0.5)

# Налаштування графіку
ax.set_xlabel('HDL_mg_dL (X1)', fontweight='bold')
ax.set_ylabel('LDL_mg_dL (X2)', fontweight='bold')
ax.set_zlabel('Hemoglobin_g_dL (Y)', fontweight='bold')
ax.set_title('Візуалізація множинної лінійної регресії (3D)', fontsize=16)

# Додаємо легенду (оскільки plot_surface не підтримує 'label', потрібен трюк)
from matplotlib.patches import Patch
fake_legend_patch = Patch(color=plt.cm.viridis(0.5), label='Побудована регресійна модель (площина)')
ax.legend(handles=[fake_legend_patch], loc='upper left')

# Збереження файлу
output_filename = 'mlr_3d_plot.png'
plt.savefig(output_filename)

print(f"3D візуалізацію збережено у файл '{output_filename}'")