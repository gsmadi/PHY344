import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm

L = 1.18E-3  # [kg*m^2]
delta_L = 0.08E-3  # [kg*m^2]
delta_T = 0.1  # [s]

current = np.array([1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0])
b_field = np.array([0.0015, 0.00225, 0.0030, 0.0038,
                    0.0045, 0.0053, 0.0060])
delta_B = np.sqrt(2.28E-8 + (1.70E-10)*current**2)

precessional_freq = np.array([0.5661, 0.8727, 1.239, 1.532, 1.765,
                              2.108, 2.379])
period = np.array([11.10, 7.20, 5.07, 4.10, 3.56, 2.98, 2.64])
delta_pf = 2*np.pi*delta_T/period**2

model = sm.OLS(precessional_freq, b_field)
fit = model.fit()
slope = fit.params[0]
slope_uncertainty = fit.bse[0]

y_fit = slope*np.linspace(0.001, 0.007, num=50)

mu = slope*L
delta_mu = np.sqrt((delta_L/L)**2 + (slope_uncertainty/slope)**2)


print "Slope: {} +/- {}".format(slope, slope_uncertainty)
print "\n\nmu = {} +/- {}".format(mu, delta_mu)

# Plot data points and quadratic fit
fig, ax = plt.subplots()

ax.plot(np.linspace(0.001, 0.007, num=50), y_fit, label="Fit", linestyle="--")

ax.errorbar(b_field, precessional_freq, fmt='o', label="Observed",
            xerr=[delta_B, delta_B],
            yerr=[delta_pf, delta_pf])

ax.set(title="Precessional motion of spinning sphere",
       xlabel="Magnetic field stength (T)",
       ylabel="Precessional frequency (Hz)")
ax.legend(loc='upper left')
plt.grid(True)
fig.savefig('plots/prec_freq.png', dpi=800)
fig.show()
