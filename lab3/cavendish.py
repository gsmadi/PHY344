
import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import optimize


def func(t, A, tau, T, phi, C):
    """Function to fit data."""
    return A*np.exp(-t/tau)*np.cos(2.0*math.pi*t/T + phi) + C


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
phi = 1.0

guess_params1 = [A, tau, T, phi, S_1]

param_fit1, pcov1 = optimize.curve_fit(func, 30*pos1[num],
                                       pos1[pos], p0=guess_params1,
                                       sigma=0.1)

# Extract estimates from position 1 fit function
A_1 = param_fit1[0]
tau_1 = param_fit1[1]
T_1 = param_fit1[2]
phi_1 = param_fit1[3]
S_1 = param_fit1[4]

# Extract errors
perr1 = np.sqrt(np.diag(pcov1))

delta_A_1 = perr1[0]
delta_tau_1 = perr1[1]
delta_S_1 = perr1[4]
delta_T_1 = perr1[2]
delta_phi_1 = perr1[3]

y_fit1 = func(30*pos1[num], A_1, tau_1, T_1, phi_1, S_1)

print "Optiimized fit parameters in position I"
print "A = {0} +/- {1}".format(A_1, delta_A_1)
print "tau = {0} +/- {1}".format(tau_1, delta_tau_1)
print "T = {0} +/- {1}".format(T_1, delta_T_1)
print "phi = {0} +/- {1}".format(phi_1, delta_phi_1)
print "S_1 = {0} +/- {1}".format(S_1, delta_S_1)
print ""

# Fit data from position 2 reading with fit function
# Initial parameter guess for position 2
S_2 = 9.6
T = 600.0
A = 6.0
tau = 500.0
phi = 1.0

guess_params2 = [A, tau, T, phi, S_2]

param_fit2, pcov2 = optimize.curve_fit(func, 30*pos2[num],
                                       pos2[pos], p0=guess_params2,
                                       sigma=0.1)

# Extract estimates from position 2 fit function
A_2 = param_fit2[0]
tau_2 = param_fit2[1]
T_2 = param_fit2[2]
phi_2 = param_fit2[3]
S_2 = param_fit2[4]
# Extract errors
perr2 = np.sqrt(np.diag(pcov2))

delta_A_2 = perr2[0]
delta_tau_2 = perr2[1]
delta_S_2 = perr2[4]
delta_T_2 = perr2[2]
delta_phi_2 = perr2[3]

y_fit2 = func(30*pos2[num], A_2, tau_2, T_2, phi_2, S_2)

print "Optiimized fit parameters in position I"
print "A = {0} +/- {1}".format(A_2, delta_A_2)
print "tau = {0} +/- {1}".format(tau_2, delta_tau_2)
print "T = {0} +/- {1}".format(T_2, delta_T_2)
print "phi = {0} +/- {1}".format(phi_2, delta_phi_2)
print "S_2 = {0} +/- {1}".format(S_2, delta_S_2)
print ""

# Prepare computed fit values for computations
# Average Period

S_1
T = (T_1 + T_2)/2.0
S_1 = S_1*1e-2
S_2 = S_2*1e-2
delta_S_1 = delta_S_1*1e-2
delta_S_2 = delta_S_2*1e-2
delta_T = delta_T_1 + delta_T_2

# Compute estimate of graviational constant G
G_computed = (math.pi**2)*(b**2)*d*(S_1 - S_2)*L_0 / \
             (m_1*(T**2)*((L_0**2) + (L_1**2)))
computed_discrepancy = G_computed - G
computed_error = ((G_computed - G)/G)*100
# Compute the uncertainty of G estimate
delta_G_computed = G_computed * \
                   math.sqrt(((delta_S_1**2 + delta_S_2**2)/(S_1 - S_2)**2) +
                             (delta_L_0/L_0)**2 + (2*delta_T/T)**2 +
                             (((2*L_0*delta_L_0)**2 +
                              (2*L_1*delta_L_1)**2)/(L_0**2 + L_1**2)))

# Compute G correction due to antitorque moment
G_corrected = G_computed * K
corrected_discrepancy = G_corrected - G
corrected_error = ((G_corrected - G)/G)*100
# Corrected uncertainty in G
delta_G_corrected = delta_G_computed * K

# Print results
print "Results of graviational constant G"
print "G_actual = {0} m^3 kg^-1 s^-2".format(G)
print ""
print "G_computed = {0} +/- {1} m^3 kg^-1 s^-2".format(G_computed,
                                                       delta_G_computed)
print "Discrepancy = {0}".format(computed_discrepancy)
print "Percentage error = {0}%".format(computed_error)
print ""
print "G_corrected = {0} +/- {1} m^3 kg^-1 s^-2".format(G_corrected,
                                                        delta_G_corrected)
print "Discrepancy = {0}".format(corrected_discrepancy)
print "Percentage error = {0}%".format(corrected_error)

# Plot data
pos1_plot, ax1 = plt.subplots()
pos2_plot, ax2 = plt.subplots()

# Position 1 plot
ax1.plot(30*pos1[num], pos1[pos], label="Observed", linestyle="", marker=".")
ax1.plot(30*pos1[num], y_fit1, label="Fit", linestyle="--",
         color='orange', linewidth=2)

ax1.set(title="Displacement S_I in position I",
        xlabel="Time (s)", ylabel="Displacement S (cm)",
        ylim=[0, 20])
ax1.legend(loc="upper right")
ax1.grid(True)

# Position 2 plot
ax2.plot(30*pos2[num], pos2[pos], label="Observed", linestyle="", marker=".")
ax2.plot(30*pos2[num], y_fit2, label="Fit", linestyle="--",
         color='orange', linewidth=2)

ax2.set(title="Displacement S_II in position II", xlabel="Time (s)",
        ylabel="Displacement S (cm)",
        ylim=[-2, 12])
ax2.legend(loc="upper right")
ax2.grid(True)

# Save plots
pos1_plot.savefig("plots/pos1_datafit.png", dpi=200)
pos2_plot.savefig("plots/pos2_datafit.png", dpi=200)
