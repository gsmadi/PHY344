
import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import optimize
import statsmodels.api as sm


def func(t, A, tau, C):
    """Function to fit data."""
    return A*np.exp(-tau*t) + C


# Column names
time = 'time'
curr_0 = 'I=0.15'
curr_1 = 'I=0.25'
curr_2 = 'I=0.35'
curr_3 = 'I=0.45'

column_names = [time, curr_0, curr_1, curr_2, curr_3]

data = pd.read_csv("data/decay.csv", header=None,
                   names=column_names)

current = [0.15, 0.25, 0.35, 0.45]
current_error = np.array([0.01, 0.02, 0.02, 0.03])
time_error = 0.5*np.ones(10)

# Optimized parameters
gamma_0 = 0.0
delta_gamma_0 = 0.0
gamma_1 = 0.0
delta_gamma_1 = 0.0
gamma_2 = 0.0
delta_gamma_2 = 0.0
gamma_3 = 0.0
delta_gamma_3 = 0.0

guess = [14.0, 0.01, 0.01]

param_fit, pcov = optimize.curve_fit(func, data[time], data[curr_0],
                                     p0=guess, sigma=0.1)
perr = np.sqrt(np.diag(pcov))

gamma_0 = 2*param_fit[1]
delta_gamma_0 = perr[1]

y_fit_0 = func(data[time], param_fit[0], param_fit[1], param_fit[2])


param_fit, pcov = optimize.curve_fit(func, data[time], data[curr_1],
                                     p0=guess, sigma=0.1)
perr = np.sqrt(np.diag(pcov))

gamma_1 = 2*param_fit[1]
delta_gamma_1 = perr[1]

y_fit_1 = func(data[time], param_fit[0], param_fit[1], param_fit[2])


param_fit, pcov = optimize.curve_fit(func, data[time], data[curr_2],
                                     p0=guess, sigma=0.1)
perr = np.sqrt(np.diag(pcov))

gamma_2 = 2*param_fit[1]
delta_gamma_2 = perr[1]

y_fit_2 = func(data[time], param_fit[0], param_fit[1], param_fit[2])


param_fit, pcov = optimize.curve_fit(func, data[time], data[curr_3],
                                     p0=guess, sigma=0.1)
perr = np.sqrt(np.diag(pcov))

gamma_3 = 2*param_fit[1]
delta_gamma_3 = perr[1]

y_fit_3 = func(data[time], param_fit[0], param_fit[1], param_fit[2])

print 'Optimized gamma parameters for damping currents:'
print 'I = 0.15, gamma = {} +/- {}'.format(gamma_0, delta_gamma_0)
print 'I = 0.25, gamma = {} +/- {}'.format(gamma_1, delta_gamma_1)
print 'I = 0.35, gamma = {} +/- {}'.format(gamma_2, delta_gamma_2)
print 'I = 0.45, gamma = {} +/- {}'.format(gamma_3, delta_gamma_3)

gammas = [gamma_0, gamma_1, gamma_2, gamma_3]
gamma_errors = np.array([delta_gamma_0, delta_gamma_1,
                         delta_gamma_2, delta_gamma_3])

model = sm.OLS(gammas, current)
fit = model.fit()
slope = fit.params[0]

y_fit = slope*np.array(current)

# Plot data
decay, ax = plt.subplots()
gamma_plot, ax1 = plt.subplots()

ax.plot(data[time].as_matrix(), data[curr_0], label=r"$\ I = 0.15 A$",
        linestyle="", marker="o", color='blue')
ax.plot(data[time].as_matrix(), y_fit_0, label='', linestyle="--", color='blue')

ax.plot(data[time], data[curr_1], label=r"$\ I = 0.25 A$", linestyle="",
        marker="o", color='red')
ax.plot(data[time].as_matrix(), y_fit_1, label='', linestyle="--", color='red')

ax.plot(data[time], data[curr_2], label=r"$\ I = 0.35 A$", linestyle="",
        marker="o", color='green')
ax.plot(data[time].as_matrix(), y_fit_2, label='', linestyle="--", color='green')

ax.plot(data[time], data[curr_3], label=r"$\ I = 0.45 A$", linestyle="",
        marker="o", color='orange')
ax.plot(data[time].as_matrix(), y_fit_3, label='', linestyle="--",
        color='orange')

ax.set(title="Torsion Pendulum damping current decay",
       xlabel="Time (s)", label='', ylabel="Amplitude (cm)")
ax.legend(loc="lower left")
ax.grid(True)

ax1.errorbar(current, gammas, marker='^', linestyle='', color='orange',
             xerr=[current_error, current_error],
             yerr=[gamma_errors, gamma_errors])
ax1.plot(current, y_fit, label='Fit', linestyle='--', color='orange')
ax1.set(title="Damping rate vs. Electromagnet current",
        xlabel="Current (A)", label='', ylabel=r"Damping rate - $\gamma$")
ax1.legend(loc="upper left")
ax1.grid(True)

decay.savefig("plots/decay.png", dpi=300)
gamma_plot.savefig("plots/gamma.png", dpi=300)
