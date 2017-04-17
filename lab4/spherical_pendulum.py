import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm

I = 4.7E-5  # [kg*m^2]
delta_I = 0.3E-5  # [kg*m^2]
delta_T = 0.01  # [s]

current = np.array([2.5, 2.7, 2.9, 3.1, 3.3, 3.4, 3.7, 3.8, 4.0])
inverse_b_field = np.array([666.67, 476.19, 370.37, 303.03, 256.41,
                           222.22, 196.08, 175.44, 158.73])
delta_inverse_B = np.sqrt(2.28E-8 + (1.70E-10)*current**2)

period_squared = np.array([2.859, 2.042, 1.703, 1.407, 1.184, 0.9487, 0.9226,
                           0.8254, 0.7841])
delta_period_squared = 2 * np.sqrt(period_squared) * delta_T

model = sm.OLS(period_squared, inverse_b_field)
fit = model.fit()
slope = fit.params[0]
slope_uncertainty = fit.bse[0]

y_fit = slope*np.linspace(100, 700, num=50)

mu = 4*I*(np.pi**2)/slope
delta_mu = np.sqrt((0.3/4.7)**2 + (0.006/4.415)**2)


print "Slope: {} +/- {}".format(slope, slope_uncertainty)
print "\n\nmu = {} +/- {}".format(mu, delta_mu)

# Plot data points and quadratic fit
fig, ax = plt.subplots()

ax.plot(np.linspace(100, 700, num=50), y_fit, label="Fit", linestyle="--")

ax.errorbar(inverse_b_field, period_squared, fmt='o', label="Observed",
            xerr=[delta_inverse_B, delta_inverse_B],
            yerr=[delta_period_squared, delta_period_squared])

ax.set(title="Harmonic Oscillation of a spherical pendulum",
       xlabel="Inverse magnetic field stength (1/T)",
       ylabel="Square of the period (s^2)")
ax.legend(loc='upper left')
plt.grid(True)
fig.savefig('plots/spherical_pendulum.png', dpi=800)
fig.show()
