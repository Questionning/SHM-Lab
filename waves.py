import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


m = np.array([0.15,
0.2,
0.25,
0.3,
0.35,
0.4,
0.45,
0.5,
0.55,
0.6,
0.65,
0.7,
0.75,
0.8,
0.85,
0.9])      
T = np.array([0.19316025, 0.25857225, 0.31640625, 0.39125025, 0.438244, 0.50098084, 0.57532225, 0.652864, 0.70476025, 0.77352025, 0.831744, 0.913936, 0.95355225, 1.018081, 1.10565225, 1.15670025])     
sigma_T = np.array([
    0.00879,
    0.01017,
    0.01125,
    0.01251,
    0.01324,
    0.014156,
    0.01517,
    0.01616,
    0.01679,
    0.01759,
    0.01824,
    0.01912,
    0.01953,
    0.02018,
    0.02103,
    0.02151
]) 


def linear_model(m, a, b):
    return a * m + b

popt, pcov = curve_fit(linear_model, m, T, sigma=sigma_T, absolute_sigma=True)
a, b = popt
a_err, b_err = np.sqrt(np.diag(pcov))

print(f"Slope (k) = {a:.4f} ± {a_err:.10f}")
print(f"Intercept = {b:.4f} ± {b_err:.4f}")


# Plot
plt.errorbar(m, T, yerr=sigma_T, fmt='o', capsize=4, label="Data with error bars")
plt.plot(m, linear_model(m, *popt), 'r-', label=f"Fit: T = ({a:.3f}±{a_err:.4f})m ({b:.4f} ± {b_err:.4f})")
plt.title("Spring Moving in SHM With Unknown Spring Constant")
plt.xlabel("Mass (kg)")
plt.ylabel("Period squared (s^2)")
plt.legend()
plt.show()
