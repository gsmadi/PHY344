import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Read data points
values = pd.read_csv('data/length_td.csv', header=None,
                     names=['Length', 'Length Uncertainties', 'Time Delay',
                            'Time Delay Uncertainties'],
                     nrows=5)

max_length = values['Length'].max()
min_length = values['Length'].min()


coefficients, residuals = np.polyfit(values['Length'], values['Time Delay'],
                                     deg=1, cov=True)

slope = coefficients[0]
slope_uncertainty = residuals[0][0]

intercept = coefficients[1]
intercept_uncertainty = residuals[1][1]

print ("Slope: {0}, Uncertainty: {1}".format(slope, slope_uncertainty))
print ("intercept: {0}, Uncertainty: {1}".format(intercept,
       intercept_uncertainty))

fig, ax = plt.subplots()

ax.errorbar(values['Length'], values['Time Delay'],
            label="Observed datapoints",
            fmt="o", linestyle="", yerr=values['Time Delay Uncertainties'],
            xerr=values['Length Uncertainties'])


lengths = np.linspace(min_length - min_length*0.5, max_length + max_length*0.5,
                      num=50)
fit = slope*lengths + intercept

ax.plot(lengths, fit, label="Linear fit", linestyle="--")

ax.set(title="TL Length vs. Time Delay", xlabel="Length (m)",
       ylabel="Time Delay (ns)")
ax.legend(loc='upper left')
plt.grid(True)
fig.savefig('plots/wave_speed.png')
fig.show()
