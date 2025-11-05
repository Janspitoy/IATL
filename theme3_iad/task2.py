import numpy as np
import matplotlib.pyplot as plt

# Параметри моделі
np.random.seed(42)
n = 50       # кількість спостережень
a = 0.1      # тренд (напрямок)
sigma = 0.2  # стандартне відхилення шуму

# Генеруємо випадкове блукання з трендом
e = np.random.normal(0, sigma, n)
Y = np.zeros(n)
Y[0] = 1  # початкове значення
for t in range(1, n):
    Y[t] = Y[t-1] + a + e[t]

# Прогноз на τ кроків уперед
tau = 10
forecast = Y[-1] + a * np.arange(1, tau+1)

# Теоретична похибка прогнозу
rmse = sigma * np.sqrt(np.arange(1, tau+1))

# Межі 95% довірчого інтервалу прогнозу
upper = forecast + 1.96 * rmse
lower = forecast - 1.96 * rmse

# Побудова графіка
plt.figure(figsize=(9, 5))
plt.plot(Y, label="Випадкове блукання з трендом", color="blue")
plt.plot(range(n-1, n+tau), np.concatenate(([Y[-1]], forecast)), 'r--', label="Прогноз")
plt.fill_between(range(n, n+tau), lower, upper, color="orange", alpha=0.3, label="95% інтервал")
plt.title("Випадкове блукання з напрямом (трендом) і прогноз на τ кроків уперед")
plt.xlabel("t")
plt.ylabel("Y(t)")
plt.legend()
plt.grid(True)
plt.show()
