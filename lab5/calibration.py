import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm

values = pd.read_csv('data/calibration.csv', header=None,
                     names=['percent', 'period', 'voltage'])

model = sm.OLS(1.0/values['period'], values['voltage'])
fit = model.fit()
slope = fit.params[0]
slope_uncertainty = fit.bse[0]

y_fit = slope*values['voltage'].as_matrix()

print "slope: {} +/- {}".format(slope, slope_uncertainty)

# Plot data points and quadratic fit
fig, ax = plt.subplots()

ax.plot(values['voltage'], y_fit, label="Fit", linestyle="--")

ax.errorbar(values['voltage'].as_matrix(), 1/values['period'].as_matrix(),
            fmt='o', label="Measured")

ax.set(title="Driver motor calibration",
       xlabel="Voltage (V)",
       ylabel="Frequency (Hz)")
ax.legend(loc='upper left')
ax.text(0.80, 0.45, r'$\ y_{fit} = 0.072x$', horizontalalignment='center',
        verticalalignment='center',
        transform=ax.transAxes, fontsize=16)
plt.grid(True)
fig.savefig('plots/calibration.png', dpi=200)
fig.show()
