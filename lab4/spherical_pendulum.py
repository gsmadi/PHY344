import matplotlib.pyplot as plt
import numpy as np

I = 4.7  # [kg*m^2]
delta_I = 0.3  # [kg*m^2]

current = np.array([2.5, 2.7, 2.9, 3.1, 3.3, 3.4, 3.7, 3.8, 4.0])
inverse_b_field = np.array([666.67, 476.19, 370.37, 303.03, 256.41,
                           222.22, 196.08, 175.44, 158.73])


period_squared = np.array([2.859, 2.042, 1.703, 1.407, 1.184, 0.9487, 0.9226,
                           0.8254, 0.7841])

coefficients, residuals = np.polyfit(inverse_b_field, period_squared, deg=1,
                                     cov=True)

y_fit = coefficients[0]*np.linspace(100, 700, num=50) + coefficients[1]

slope = coefficients[0]
intercept = coefficients[1]

slope_uncertainty = np.sqrt(residuals[0][0])
intercept_uncertainty = np.sqrt(residuals[1][1])

mu = I*4*np.pi**2/slope

print "Slope: {} +/- {}".format(slope, slope_uncertainty)
print "Intercept: {} +/- {}".format(intercept, intercept_uncertainty)
print "\n\nmu = {} +/- {}".format(mu, 0.1)

# Plot data points and quadratic fit
fig, ax = plt.subplots()

ax.plot(np.linspace(100, 700, num=50), y_fit, label="Fit", linestyle="--")

ax.errorbar(inverse_b_field, period_squared, fmt='o', label="Observed")

ax.set(title="Harmonic Oscillation of a spherical pendulum",
       xlabel="Inverse magnetic field stength (1/T)",
       ylabel="Square of the period (s^2)")
ax.legend(loc='upper left')
plt.grid(True)
fig.set_dpi(800)
fig.savefig('plots/spherical_pendulum.png')
fig.show()
