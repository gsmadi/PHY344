import matplotlib.pyplot as plt
import numpy as np

m = 1.3E-3  # [kg]
delta_m = 0.1E-3  # [kg]
g = 9.8  # [m*s^2]

current = np.array([2.5, 2.7, 2.9, 3.1, 3.3, 3.4, 3.7, 3.8, 4.0])
b_field = np.array([0.00375, 0.00405, 0.00435, 0.00465, 0.00495,
                    0.00510, 0.00555, 0.00570, 0.0060])
delta_B = np.sqrt(2.28E-8 + (1.70E-10)*current**2)

r = np.array([6.7, 7.8, 8.7, 10.2, 10.6, 11.4, 12.3, 12.8, 14.0])
delta_r = 0.3*np.ones(len(r))  # [cm]

coefficients, residuals = np.polyfit(b_field, r, deg=1, cov=True)

y_fit = coefficients[0]*np.linspace(0.003, 0.007, num=50) + coefficients[1]

slope = coefficients[0]*1E-2
intercept = coefficients[1]*1E-2

slope_uncertainty = np.sqrt(residuals[0][0])*1E-2
intercept_uncertainty = np.sqrt(residuals[1][1])*1E-2

mu = m*g*slope
delta_mu = mu * np.sqrt((delta_m/m)**2 + (slope_uncertainty/slope)**2)

print "Slope: {} +/- {}".format(slope, slope_uncertainty)
print "Intercept: {} +/- {}".format(intercept, intercept_uncertainty)
print "\n\nmu = {} +/- {}".format(mu, delta_mu)

# Plot data points and quadratic fit
fig, ax = plt.subplots()

ax.plot(np.linspace(0.003, 0.007, num=50), y_fit, label="Fit", linestyle="--")

ax.errorbar(b_field, r, xerr=[delta_B, delta_B],
            yerr=[delta_r, delta_r], fmt='o', label="Observed")

ax.set(title="Magnetic torque equals Gravitational torque",
       xlabel="Magnetic field stength (T)",
       ylabel="Radius (cm)")
ax.legend(loc='upper left')
plt.grid(True)
fig.savefig('plots/mag_grav.png', dpi=800)
fig.show()
