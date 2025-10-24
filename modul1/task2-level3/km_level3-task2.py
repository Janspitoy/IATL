import pandas as pd
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('lipoproteins_hemoglobin_dataset.csv')

# Перевірка наявності необхідних колонок
required_cols = ['HDL_mg_dL', 'LDL_mg_dL', 'Hemoglobin_g_dL']
if not all(col in df.columns for col in required_cols):
    print(f"Помилка: У файлі відсутні необхідні колонки. Потрібні: {required_cols}")
    exit()

# Обчислення матриці кореляцій
corr_matrix = df.corr()

# Обчислення коефіцієнтів кореляції Пірсона з p-значеннями
r_hdl_hb, p_hdl_hb = pearsonr(df['HDL_mg_dL'], df['Hemoglobin_g_dL'])
r_ldl_hb, p_ldl_hb = pearsonr(df['LDL_mg_dL'], df['Hemoglobin_g_dL'])

# Виведення результатів
print("Матриця кореляцій (Pearson r):")
print(corr_matrix)

print("\nДетальні коефіцієнти кореляції з p-значеннями:")
print(f"HDL та Hb: r = {r_hdl_hb:.3f}, p = {p_hdl_hb:.3f}")
print(f"LDL та Hb: r = {r_ldl_hb:.3f}, p = {p_ldl_hb:.3f}")

print("\nСтворення візуалізації...")

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Графік 1: HDL vs Hemoglobin
sns.regplot(ax=axes[0], x='HDL_mg_dL', y='Hemoglobin_g_dL', data=df,
            line_kws={"color":"red"}, scatter_kws={"alpha":0.5})
axes[0].set_title(f'HDL vs Hemoglobin\nr = {r_hdl_hb:.3f}, p = {p_hdl_hb:.3f}', fontsize=14)
axes[0].set_xlabel('Ліпопротеїни (HDL) (mg/dL)', fontsize=12)
axes[0].set_ylabel('Гемоглобін (g/dL)', fontsize=12)
axes[0].grid(True, linestyle='--', alpha=0.6)

# Графік 2: LDL vs Hemoglobin
sns.regplot(ax=axes[1], x='LDL_mg_dL', y='Hemoglobin_g_dL', data=df,
            line_kws={"color":"red"}, scatter_kws={"alpha":0.5})
axes[1].set_title(f'LDL vs Hemoglobin\nr = {r_ldl_hb:.3f}, p = {p_ldl_hb:.3f}', fontsize=14)
axes[1].set_xlabel('Ліпопротеїни (LDL) (mg/dL)', fontsize=12)
axes[1].set_ylabel('') # Прибираємо дублюючу мітку осі Y
axes[1].grid(True, linestyle='--', alpha=0.6)

# Покращуємо загальний вигляд
plt.tight_layout()

# Збереження файлу
output_filename = 'correlations_plot.png'
plt.savefig(output_filename)

print(f"Візуалізацію збережено у файл '{output_filename}'")