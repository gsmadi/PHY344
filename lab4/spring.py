import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm

z = np.array([0.8E-2, 1.5E-2, 2.3E-2, 2.9E-2])
delta_z = 0.2E-2*np.ones(4)

mg = np.array([0.0098, 0.0196, 0.0294, 0.0392])

model = sm.OLS(mg, z)
fit = model.fit()
slope = fit.params[0]
slope_uncertainty = fit.bse[0]
y_fit = slope*np.linspace(0.006, 0.04, num=50)

k = slope

print "k: {} +/- {}".format(k, slope_uncertainty)

# Plot data points and quadratic fit
fig, ax = plt.subplots()

ax.plot(np.linspace(0.006, 0.04, num=50), y_fit, label="Fit", linestyle="--")

ax.errorbar(z, mg, fmt='o', label="Observed",
            xerr=[delta_z, delta_z])

ax.set(title="Spring constant of suspended magnet",
       xlabel="Displacement (m)",
       ylabel="Force (N)")
ax.legend(loc='upper left')
plt.grid(True)
fig.savefig('plots/spring.png', dpi=800)
fig.show()
