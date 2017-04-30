import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm

values = pd.read_csv('data/cycles.csv', header=None,
                     names=['c1', 'c2', 'c3'])

errors = []
time = []
cycles = np.linspace(1, 10, num=10)
errors
for i in range(0, 10):
    mean = values.stack()[i].mean()
    std = values.stack()[i].std()

    time.append(mean)
    errors.append(std)

model = sm.OLS(time, cycles)
fit = model.fit()
slope = fit.params[0]
slope_uncertainty = fit.bse[0]

y_fit = slope*cycles

print "slope: {} +/- {}".format(slope, slope_uncertainty)

# Plot data points and quadratic fit
fig, ax = plt.subplots()

ax.plot(cycles, y_fit, label="Fit", linestyle="--")

ax.errorbar(cycles, time, fmt='o', label="Measured",
            xerr=[errors, errors])

ax.set(title="Time intervals per cycles",
       xlabel="Cycles",
       ylabel="Time Interval (s)")
ax.legend(loc='upper left')
ax.text(0.80, 0.45, r'$\ y_{fit} = 1.905x$', horizontalalignment='center',
        verticalalignment='center',
        transform=ax.transAxes, fontsize=16)
plt.grid(True)
fig.savefig('plots/cycles.png', dpi=800)
fig.show()
