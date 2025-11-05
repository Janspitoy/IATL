import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Дані часового ряду
y = np.array([1.6, 0.8, 1.2, 0.5, 0.9, 1.1, 1.1, 0.6, 1.5, 0.8, 0.9, 1.2, 0.5, 1.3, 0.8, 1.2])

# (а) Побудова графіка часового ряду
plt.figure(figsize=(8, 4))
plt.plot(y, marker='o')
plt.title("Часовий ряд з 16 спостережень")
plt.xlabel("t")
plt.ylabel("y(t)")
plt.grid(True)
plt.show()

# (в) Обчислення коефіцієнта автокореляції першого порядку
y_mean = np.mean(y)
autocorr_1 = np.corrcoef(y[:-1], y[1:])[0, 1]
autocorr_1
