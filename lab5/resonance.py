
import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import optimize

# Read data
data = pd.read_csv("data/resonance.csv", header=None,
                   names=['voltage', 'I=0.15', 'I=0.25',
                          'I=0.35', 'I=0.45'])
values = pd.read_csv('data/calibration.csv', header=None,
                     names=['percent', 'period', 'voltage'])

# Calibration computations
omegas = 2*np.pi*0.072*data['voltage'].as_matrix()
voltage = data['voltage'].as_matrix()
period = values['period'].as_matrix()
delta_omegas = np.sqrt((0.002/0.072)**2 + (0.05/period)**2 + (0.01/voltage)**2)
delta_theta = 0.2*np.ones(8)
theta_d = 0.4
omega_naught = 3.29
omegas
damping_rates = np.array([0.07, 0.10, 0.18, 0.25])
omega_d = np.linspace(1, 6, num=500)
delta_omegas
# I = 0.15
theta_1 = theta_d/np.sqrt((1-(omega_d/omega_naught)**2)**2 +
                          (damping_rates[0]*omega_d/omega_naught**2)**2)

# I = 0.25
theta_2 = theta_d/np.sqrt((1-(omega_d/omega_naught)**2)**2 +
                          (damping_rates[1]*omega_d/omega_naught**2)**2)
# I = 0.35
theta_3 = theta_d/np.sqrt((1-(omega_d/omega_naught)**2)**2 +
                          (damping_rates[2]*omega_d/omega_naught**2)**2)
# I = 0.45
theta_4 = theta_d/np.sqrt((1-(omega_d/omega_naught)**2)**2 +
                          (damping_rates[3]*omega_d/omega_naught**2)**2)


# Plot data
damp1, ax = plt.subplots()
damp2, ax1 = plt.subplots()
damp3, ax2 = plt.subplots()
damp4, ax3 = plt.subplots()

ax.errorbar(omegas, data['I=0.15'].as_matrix(), label="Measured",
            xerr=[delta_omegas, delta_omegas], linestyle="", marker="o",
            yerr=[delta_theta, delta_theta], color='red')
ax.plot(omega_d, theta_1, label='Theoretical', linestyle="--", color='blue')

ax1.errorbar(omegas, data['I=0.25'].as_matrix(), label="Measured", linestyle="",
             xerr=[delta_omegas, delta_omegas], marker="o", color='red',
             yerr=[delta_theta, delta_theta])
ax1.plot(omega_d, theta_2, label='Theoretical', linestyle="--", color='blue')

ax2.errorbar(omegas, data['I=0.35'].as_matrix(), label="Measured", linestyle="",
             xerr=[delta_omegas, delta_omegas], marker="o", color='red',
             yerr=[delta_theta, delta_theta])
ax2.plot(omega_d, theta_3, label='Theoretical', linestyle="--", color='blue')

ax3.errorbar(omegas, data['I=0.45'].as_matrix(), label="Measured", linestyle="",
             xerr=[delta_omegas, delta_omegas], marker="o", color='red',
             yerr=[delta_theta, delta_theta])
ax3.plot(omega_d, theta_4, label='Theoretical', linestyle="--",
         color='blue')

ax.set(title="Torsion pendulum frequency response for I = 0.15 A",
       xlabel="Driving frequency (s^-1)", label='', ylabel=r"Amplitude")
ax.legend(loc="upper left")
ax.grid(True)

ax1.set(title="Torsion pendulum frequency response for I = 0.25 A",
        xlabel="Driving frequency (s^-1)", label='', ylabel=r"Amplitude")
ax1.legend(loc="upper left")
ax1.grid(True)

ax2.set(title="Torsion pendulum frequency response for I = 0.35 A",
        xlabel="Driving frequency (s^-1)", label='', ylabel=r"Amplitude")
ax2.legend(loc="upper left")
ax2.grid(True)

ax3.set(title="Torsion pendulum frequency response for I = 0.45 A",
        xlabel="Driving frequency (s^-1)", label='', ylabel=r"Amplitude")
ax3.legend(loc="upper left")
ax3.grid(True)

damp1.savefig("plots/damp1.png", dpi=300)
damp2.savefig("plots/damp2.png", dpi=300)
damp3.savefig("plots/damp3.png", dpi=300)
damp4.savefig("plots/damp4.png", dpi=300)
