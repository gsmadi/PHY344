import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm

values = pd.read_csv('data/cycles.csv', header=None,
                     names=['c1', 'c2', 'c3'])

values_15 = pd.read_csv('data/cycles_15.csv', header=None,
                        names=['c1', 'c2', 'c3'])

values_25 = pd.read_csv('data/cycles_25.csv', header=None,
                        names=['c1', 'c2', 'c3'])

values_35 = pd.read_csv('data/cycles_35.csv', header=None,
                        names=['c1', 'c2', 'c3'])

values_45 = pd.read_csv('data/cycles_45.csv', header=None,
                        names=['c1', 'c2', 'c3'])

errors_0 = []
errors_1 = []
errors_2 = []
errors_3 = []
errors_4 = []

interval_0 = []
interval_1 = []
interval_2 = []
interval_3 = []
interval_4 = []


cycles = np.linspace(1, 10, num=10)

for i in range(0, 10):
    mean = values.stack()[i].mean()
    std = values.stack()[i].std()

    interval_0.append(mean)
    errors_0.append(std)

    mean = values_15.stack()[i].mean()
    std = values_15.stack()[i].std()

    interval_1.append(mean)
    errors_1.append(std)

    mean = values_25.stack()[i].mean()
    std = values_25.stack()[i].std()

    interval_2.append(mean)
    errors_2.append(std)

    mean = values_35.stack()[i].mean()
    std = values_35.stack()[i].std()

    interval_3.append(mean)
    errors_3.append(std)

    mean = values_45.stack()[i].mean()
    std = values_45.stack()[i].std()

    interval_4.append(mean)
    errors_4.append(std)

damping_errors = 0.1*np.ones(10)

model = sm.OLS(interval_0, cycles)
fit = model.fit()
slope_0 = fit.params[0]
slope_uncertainty_0 = fit.bse[0]

model = sm.OLS(interval_1, cycles)
fit = model.fit()
slope_1 = fit.params[0]
slope_uncertainty_1 = fit.bse[0]

model = sm.OLS(interval_2, cycles)
fit = model.fit()
slope_2 = fit.params[0]
slope_uncertainty_2 = fit.bse[0]

model = sm.OLS(interval_3, cycles)
fit = model.fit()
slope_3 = fit.params[0]
slope_uncertainty_3 = fit.bse[0]

model = sm.OLS(interval_4, cycles)
fit = model.fit()
slope_4 = fit.params[0]
slope_uncertainty_4 = fit.bse[0]

y_fit_0 = slope_0*cycles
y_fit_1 = slope_1*cycles
y_fit_2 = slope_2*cycles
y_fit_3 = slope_3*cycles
y_fit_4 = slope_4*cycles


print "slope 0: {} +/- {}".format(slope_0, slope_uncertainty_0)
print "slope 1: {} +/- {}".format(slope_1, slope_uncertainty_1)
print "slope 2: {} +/- {}".format(slope_2, slope_uncertainty_2)
print "slope 3: {} +/- {}".format(slope_3, slope_uncertainty_3)
print "slope 4: {} +/- {}".format(slope_4, slope_uncertainty_4)

# Plot data points and quadratic fit
fig, ax = plt.subplots()

ax.plot(cycles, y_fit_0, linestyle="--", color='blue')
ax.errorbar(cycles, interval_0, fmt='o', label=r'$\ I = 0.0 A$',
            yerr=[errors_0, errors_0], color='blue')


ax.plot(cycles, y_fit_1, linestyle="--", color='red')
ax.errorbar(cycles, interval_1, fmt='o', label=r'$\ I = 0.15 A$',
            yerr=[errors_1, errors_1], color='red')

ax.plot(cycles, y_fit_2, linestyle="--", color='green')
ax.errorbar(cycles, interval_2, fmt='o', label=r'$\ I = 0.25 A$',
            yerr=[errors_2, errors_2], color='green')

ax.plot(cycles, y_fit_3, linestyle="--", color='orange')
ax.errorbar(cycles, interval_3, fmt='o', label=r'$\ I = 0.35 A$',
            yerr=[errors_3, errors_3], color='orange')

ax.plot(cycles, y_fit_4, linestyle="--", color='purple')
ax.errorbar(cycles, interval_4, fmt='o', label=r'$\ I = 0.45 A$',
            yerr=[errors_4, errors_4], color='purple')


ax.set(title="Time intervals per cycles with damping",
       xlabel="Cycles",
       ylabel="Time Interval (s)")
ax.legend(loc='upper left')
plt.grid(True)
fig.savefig('plots/cycles_damping.png', dpi=800)
fig.show()
