import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.api import VAR

# 1. Дослідження структури часового ряду
np.random.seed(42)
days = pd.date_range("2025-08-01", periods=60)
trend = np.linspace(1000, 1500, 60)  # зростання популярності
seasonality = 100 * np.sin(np.arange(60) * 2 * np.pi / 7)  # тижнева циклічність
noise = np.random.normal(0, 50, 60)
requests = trend + seasonality + noise

data = pd.DataFrame({"date": days, "requests": requests})
data.set_index("date", inplace=True)

plt.figure(figsize=(10, 4))
plt.plot(data.index, data["requests"], label="Кількість запитів")
plt.title("1 Структура часового ряду: тренд і сезонність запитів до API")
plt.xlabel("Дата")
plt.ylabel("Кількість запитів")
plt.legend()
plt.grid(True)
plt.show()

# 2. Математична модель (затримка ↔ кількість користувачів)
users = np.arange(50, 1050, 50)
delay = 0.2 + 0.0008 * users + np.random.normal(0, 0.02, len(users))  # проста лінійна залежність

plt.figure(figsize=(6, 4))
plt.scatter(users, delay, color='orange')
plt.title("2 Залежність часу відгуку від кількості користувачів")
plt.xlabel("Кількість одночасних користувачів")
plt.ylabel("Середній час відгуку (сек)")
plt.grid(True)
plt.show()

# 3. Прогнозування майбутніх витрат (API costs)
months = pd.date_range("2023-01-01", periods=24, freq="M")
trend = np.linspace(200, 500, 24)
season = 30 * np.sin(np.arange(24) * 2 * np.pi / 12)
costs = trend + season + np.random.normal(0, 10, 24)

cost_series = pd.Series(costs, index=months)
model = ExponentialSmoothing(cost_series, trend='add', seasonal='add', seasonal_periods=12).fit()
forecast = model.forecast(3)

plt.figure(figsize=(8, 4))
plt.plot(cost_series, label="Історичні витрати")
plt.plot(forecast, label="Прогноз (наступний квартал)", linestyle="--")
plt.title("3 Прогнозування витрат на API (Holt-Winters)")
plt.xlabel("Місяць")
plt.ylabel("Витрати ($)")
plt.legend()
plt.grid(True)
plt.show()

# 4. Причинно-наслідкові зв’язки (шум ↔ якість)
days2 = pd.date_range("2025-08-01", periods=60)
noise_db = 40 + 5 * np.sin(np.arange(60) * 2 * np.pi / 7) + np.random.normal(0, 1, 60)
wer = 10 + 0.3 * noise_db + np.random.normal(0, 2, 60)

df_causal = pd.DataFrame({"noise_db": noise_db, "wer": wer}, index=days2)
model = VAR(df_causal)
results = model.fit(2)
print("VAR summary:")
print(results.summary())

plt.figure(figsize=(8, 4))
plt.plot(df_causal.index, df_causal["noise_db"], label="Рівень шуму (dB)")
plt.plot(df_causal.index, df_causal["wer"], label="Word Error Rate (%)")
plt.title("4 Взаємозв’язок між шумом та якістю розпізнавання")
plt.xlabel("Дата")
plt.legend()
plt.grid(True)
plt.show()

# 5. Згладжування та фільтрація
raw_delay = data["requests"].rolling(1).mean() + np.random.normal(0, 30, 60)
smoothed_delay = data["requests"].rolling(5).mean()

plt.figure(figsize=(8, 4))
plt.plot(data.index, raw_delay, color='gray', alpha=0.6, label="Сирі дані (з шумом)")
plt.plot(data.index, smoothed_delay, color='blue', label="Згладжено (ковзне середнє, k=5)")
plt.title("5 Згладжування даних часу відгуку")
plt.xlabel("Дата")
plt.ylabel("Час відгуку (умовні одиниці)")
plt.legend()
plt.grid(True)
plt.show()
