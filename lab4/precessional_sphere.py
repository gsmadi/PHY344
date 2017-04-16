import matplotlib.pyplot as plt
import numpy as np

L = 118  # [kg*m^2]
delta_I = 8  # [kg*m^2]

current = np.array([2.5, 2.7, 2.9, 3.1, 3.3, 3.4, 3.7, 3.8, 4.0])
b_field = np.array([0.0015, 0.00225, 0.0030, 0.0038,
                    0.0045, 0.0053, 0.0060])


precessional_freq = np.array([0.5661, 0.8727, 1.239, 1.532, 1.765,
                              2.108, 2.379])

coefficients, residuals = np.polyfit(b_field, precessional_freq, deg=1,
                                     cov=True)

y_fit = coefficients[0]*np.linspace(0.001, 0.007, num=50) + coefficients[1]

slope = coefficients[0]
intercept = coefficients[1]

slope_uncertainty = np.sqrt(residuals[0][0])
intercept_uncertainty = np.sqrt(residuals[1][1])

mu = slope*L

print "Slope: {} +/- {}".format(slope, slope_uncertainty)
print "Intercept: {} +/- {}".format(intercept, intercept_uncertainty)
print "\n\nmu = {} +/- {}".format(mu, 0.1)

# Plot data points and quadratic fit
fig, ax = plt.subplots()

ax.plot(np.linspace(0.001, 0.007, num=50), y_fit, label="Fit", linestyle="--")

ax.errorbar(b_field, precessional_freq, fmt='o', label="Observed")

ax.set(title="Precessional motion of spinning sphere",
       xlabel="Magnetic field stength (T)",
       ylabel="Precessional frequency (Hz)")
ax.legend(loc='upper left')
plt.grid(True)
fig.set_dpi(800)
fig.savefig('plots/prec_freq.png')
fig.show()
