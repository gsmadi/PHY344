import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm

k = 1.32
delta_k = 0.02
delta_I = 0.1
R = 0.116
delta_R = 0.001
N = 195
mu_naugth = 4*np.pi*1E-7

z = np.array([0.3E-2, 0.5E-2, 1.0E-2, 1.3E-2, 1.7E-2,
              2.0E-2, 2.3E-2, 2.6E-2])
delta_z = 0.2E-2*np.ones(8)

current = np.array([0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0])
dB_dz = ((1.5*mu_naugth*N*current)/R**2)*(4.0/5.0)**(5.0/2.0)

delta_dB_dz = dB_dz*np.sqrt((delta_I/current)**2 + (delta_R/R)**2)

model = sm.OLS(dB_dz, z)
fit = model.fit()
slope = fit.params[0]
slope_uncertainty = fit.bse[0]

y_fit = slope*np.linspace(0.001, 0.03, num=50)

mu = slope*k
delta_mu = np.sqrt((delta_k/k)**2 + (slope_uncertainty/slope))

print "mu: {} +/- {}".format(mu, delta_mu)

# Plot data points and quadratic fit
fig, ax = plt.subplots()

ax.plot(np.linspace(0.001, 0.03, num=50), y_fit, label="Fit", linestyle="--")

ax.errorbar(z, dB_dz, fmt='o', label="Observed",
            xerr=[delta_z, delta_z],
            yerr=[delta_dB_dz, delta_dB_dz])

ax.set(title="Magnetic field gradient",
       xlabel="Displacement (m)",
       ylabel="dB/dz (N)")
ax.legend(loc='upper left')
plt.grid(True)
fig.savefig('plots/gradient.png', dpi=800)
fig.show()
