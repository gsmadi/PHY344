import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

JOULE_TO_EV = 6.24E18 # [eV/J]
EV_TO_JOULES = 1.6022E-19 # [J/eV]
PLANCK_CONST = 6.63E-34 # [J*s]
SPEED_OF_LIGHT = 3.0E8 # [m*s^-1]
CHARGE_E = 1.602E-19 # [C]
POTASSIUM_WORK_FUNCTION = 3.67E-19 # [J]

frequencies = np.linspace(100, 300, num=600)

# Filter measurements
stopping_pontentials = np.array([1.227, 0.8824, 0.5584])
filter_frequencies = np.array([274E12, 229E12, 172E12])
filter_data_points = [filter_frequencies, stopping_pontentials]
coefficients, _, _, _, _ = np.polyfit(filter_data_points[0], filter_data_points[1],
                                      deg=1, full=True)
slope = coefficients[0]*1E12
intercept = coefficients[1]
observed = slope*frequencies + intercept

model_slope = (PLANCK_CONST*1E12/CHARGE_E)
model_intercept = (POTASSIUM_WORK_FUNCTION*EV_TO_JOULES*1E12/CHARGE_E)
photoelectric_model = model_slope*frequencies - model_intercept

work_function_prediction = intercept * -CHARGE_E * JOULE_TO_EV
plancks_const_prediction = coefficients[0] * CHARGE_E

# Plot data points and quadratic fit
fig, ax = plt.subplots()

ax.plot(frequencies, observed, label="Observed")

ax.plot(frequencies, photoelectric_model, label="Actual")

ax.set(title="Stopping Voltage vs. Frequency", xlabel="Frequency (THz)", ylabel="Voltage (V)")
ax.legend(loc='upper right')
plt.grid(True)
fig.savefig('plots/observation_vs_model.png')
fig.show()
