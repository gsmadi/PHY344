import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import optimize


def func(t, A, tau, omega, phi, C):
    """Function to fit data."""
    return A*np.exp(-t/tau)*np.cos(omega*t + phi) + C


# Given constants and measured values
m_1 = 1.5  # [kg] - Mass of small masses on rigid rod
d = 50e-3  # [m] - Radius of rigid rod
b = 47e-3  # [m] - Distance between m1 and m2
L_0 = 2.13  # [m] - Distance for torsion balance to glass ruler
L_1 = 5.2e-2  # [m] - Distance from null position on ruler to equlibrium point
K = 1.083  # Antitorque moment correction constant
G = 6.67408e-11  # [m^3 kg^-1 s^-2] - Actual value gravitational constant G

# Measurement uncertainties
delta_L_0 = 0.012  # [m]
delta_L_1 = 0.1e-2  # [m]

# Estimates from fit
S_1 = 0.0  # [m] - Equilibrium of torsion balance in position 1
S_2 = 0.0  # [m] - Equilibrium of torsion balance in position 2
T = 0.0   # [s] - Period of torsion balance oscillations

# Uncertainties from fit
delta_S_1 = 0.0  # [m]
delta_S_2 = 0.0  # [m]
delta_T = 0.0  # [s]

# Read data
nrows = 116

# Column names
num, pos = "Datapoint", "Position"
column_names = [num, pos]
pos1 = pd.read_csv("data/pos1_datapoints.csv", header=None,
                   names=column_names, nrows=nrows)
pos2 = pd.read_csv("data/pos2_datapoints.csv", header=None,
                   names=column_names, nrows=nrows)

# Fit data from position 1 reading with fit function
# Initial parameter guess for position 1
S_1 = 9.6
T = 600.0
A = 15.9
tau = 30.0
omega = 2*math.pi/T
phi = 1.0

guess_params1 = [A, tau, omega, phi, S_1]

param_fit1, pcov1 = optimize.curve_fit(func, 30*pos1[num],
                                       pos1[pos], p0=guess_params1,
                                       sigma=0.1)

# Extract estimates from position 1 fit function
A_1 = param_fit1[0]
tau_1 = param_fit1[1]
omega_1 = param_fit1[2]
phi_1 = param_fit1[3]
S_1 = param_fit1[4]

# Extract errors
perr1 = np.sqrt(np.diag(pcov1))

delta_S_1 = perr1[4]
delta_omega_1 = perr1[2]
delta_T_1 = 2*math.pi*delta_omega_1/omega_1**2

y_fit1 = func(30*pos1[num], A_1, tau_1, omega_1, phi_1, S_1)

# Fit data from position 2 reading with fit function
# Initial parameter guess for position 2
S_2 = 9.6
T = 600.0
A = 6.0
tau = 40.0
omega = 2*math.pi/T
phi = 1.0

guess_params2 = [A, tau, omega, phi, S_2]

param_fit2, pcov2 = optimize.curve_fit(func, 30*pos2[num],
                                       pos2[pos], p0=guess_params2,
                                       sigma=0.1)

# Extract estimates from position 2 fit function
A_2 = param_fit2[0]
tau_2 = param_fit2[1]
omega_2 = param_fit2[2]
phi_2 = param_fit2[3]
S_2 = param_fit2[4]

# Extract errors
perr2 = np.sqrt(np.diag(pcov2))

delta_S_2 = perr2[4]
delta_omega_2 = perr2[2]
delta_T_2 = 2*math.pi*delta_omega_2/omega_2**2

y_fit2 = func(30*pos2[num], A_2, tau_2, omega_2, phi_2, S_2)

# Prepare computed fit values for computations
# Average Period
T = math.pi*((1.0/abs(omega_1)) + (1.0/omega_2))
S_1 = S_1*1e-2
S_2 = S_2*1e-2
delta_T = delta_T_1 + delta_T_2

# Compute estimate of graviational constant G
G_computed = (math.pi**2)*(b**2)*d*(S_1 - S_2)*L_0 / \
             (m_1*(T**2)*((L_0**2) + (L_1**2)))

# Compute the uncertainty of G estimate
delta_G_computed = G_computed * \
                   math.sqrt(((delta_S_1**2 + delta_S_2**2)/(S_1 - S_2)**2) +
                             (delta_L_0/L_0)**2 + (2*delta_T/T)**2 +
                             (((2*L_0*delta_L_0)**2 +
                              (2*L_1*delta_L_1)**2)/(L_0**2 + L_1**2)))

# Compute G correction due to antitorque moment
G_corrected = G_computed * K

# Corrected uncertainty in G
delta_G_corrected = delta_G_computed * K

# Print results
print "Results of graviational constant G"
print "G_actual = {0} m^3 kg^-1 s^-2".format(G)
print "G_computed = {0} +/- {1} m^3 kg^-1 s^-2".format(G_computed,
                                                       delta_G_computed)
print "G_corrected = {0} +/- {1} m^3 kg^-1 s^-2".format(G_corrected,
                                                        delta_G_corrected)

# Plot data
pos1_plot, ax1 = plt.subplots()
pos2_plot, ax2 = plt.subplots()

# Position 1 plot
ax1.plot(30*pos1[num], pos1[pos], label="Observed", linestyle="", marker=".")
ax1.plot(30*pos1[num], y_fit1, label="Fit", linestyle="--")

ax1.set(title="", xlabel="Time (s)", ylabel="Displacement S (cm)",
        ylim=[0, 20])
ax1.legend(loc="upper right")
ax1.grid(True)

# Position 2 plot
ax2.plot(30*pos2[num], pos2[pos], label="Observed", linestyle="", marker=".")
ax2.plot(30*pos2[num], y_fit2, label="Fit", linestyle="--")

ax2.set(title="", xlabel="Time (s)", ylabel="Displacement S (cm)",
        ylim=[-2, 12])
ax2.legend(loc="upper right")
ax2.grid(True)

# Save plots
pos1_plot.savefig("plots/pos1_datafit.png")
pos2_plot.savefig("plots/pos2_datafit.png")
