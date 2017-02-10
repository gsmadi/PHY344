import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Read data points
values = pd.read_csv('data/filter580.csv', header=None,
                     names=['Voltage', 'Current'],
                     nrows=24)


wavelength = 580E-9 # Nanometers
frequency = (1.0/wavelength)/10**4 # THz
I_a = 0.0322  # Current plateaus at constant negative current
V_s = 0.831 # Aparent stopping potential

fit_points = values.loc[values['Current'] >= 0]
coefficients, _, _, _, _ = np.polyfit(fit_points['Voltage'], fit_points['Current'],
                                      deg=2, full=True)

# Quadratic fit of observed data points
a = coefficients[0]
quadratic_fit = a*(values['Voltage'] - V_s)**2 - I_a
# Plot data points and quadratic fit
fig, ax = plt.subplots()

observed = ax.plot(values['Voltage'], values['Current'],
                   label="Data points", marker='o', markersize=4)

fitted = ax.plot(values['Voltage'], quadratic_fit, linewidth=2,
                 linestyle="--", label="Quadratic fit")


ax.set(title="Quadratic fit - 580nm", xlabel="Voltage (V)", ylabel="Current (nA)",
       xlim=[values['Voltage'].min(), V_s + 1],
       ylim=[values['Current'].min(), values['Current'].max()])
ax.legend(loc='upper right')
plt.grid(True)
fig.savefig('plots/filter580quad.png')
fig.show()



# Plot linear fit
linear_estimate = np.sqrt(quadratic_fit - I_a)
linear_estimate
if np.isnan(linear_estimate).any():
    stop_estimate = np.where(np.isnan(linear_estimate))[0][0]

if stop_estimate != 0:
    linear_estimate = linear_estimate[0:stop_estimate]

voltages = values['Voltage'][0:linear_estimate.size]

coefficients, _, _, _, _ = np.polyfit(voltages, linear_estimate,
                                      deg=1, full=True)
slope = coefficients[0]
intercept = coefficients[1]

# Einstein photoelectric model
voltages = np.linspace(values['Voltage'].min(), values['Voltage'].max(), num=240)
linear_fit = slope * voltages + intercept
linear_fit
linear_fit = linear_fit.clip(0)
stopping_pontential = np.roots(coefficients)[0]

print "Stopping potential {:5.4} Volts at {:3.0f} THz".format(stopping_pontential, frequency)

fig2, ax2 = plt.subplots()
voltages = np.linspace(values['Voltage'].min(), values['Voltage'].max(), num=linear_fit.size)
ax2.plot(voltages, linear_fit,
                label="Stopping potential: {:5.4} V".format(stopping_pontential))

ax2.set(title="Stopping potential estimate - 580nm",
        xlabel="Voltage (V)",
        ylabel="SQRT(I - I_a) (nA)^(1/2)",
        xlim=[values['Voltage'].min(), V_s + 0.5])
ax2.legend(loc='upper right')

# No line in labels
leg = ax2.legend(handlelength=0, handletextpad=0, fancybox=True)
for item in leg.legendHandles:
    item.set_visible(False)

plt.grid(True)
fig2.savefig('plots/filter580estimate.png')
fig2.show()
