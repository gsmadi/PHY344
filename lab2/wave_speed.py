import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm

# Read data points
values = pd.read_csv('data/length_td.csv', header=None,
                     names=['Length', 'Length Uncertainties', 'Time Delay',
                            'Time Delay Uncertainties'],
                     nrows=5)

max_time = values['Time Delay'].max()
min_time = values['Time Delay'].min()


coefficients, residuals = np.polyfit(values['Length'], values['Time Delay'],
                                     deg=1, cov=True)
model = sm.OLS(values['Length'], values['Time Delay'])
results = model.fit()
model_slope = results.params[0]
model_slope_uncertainty = results.bse[0]
model_slope

slope = coefficients[0]
slope_uncertainty = residuals[0][0]

intercept = coefficients[1]
intercept_uncertainty = residuals[1][1]


print ("Slope: {0}, Uncertainty: {1}".format(model_slope*10**9,
                                             model_slope_uncertainty*10**9))


fig, ax = plt.subplots()

ax.errorbar(values['Length'], values['Time Delay'],
            label="Observed datapoints",
            fmt="o", linestyle="", yerr=values['Time Delay Uncertainties'],
            xerr=values['Length Uncertainties'])


lengths = np.linspace(min_time - min_time*0.5, max_time + max_time*0.5,
                      num=50)
fit = model_slope*lengths


ax.plot(fit, lengths, label="Linear fit", linestyle="--")

ax.set(title="TL Length vs. Time Delay", ylabel="Length (m)",
       xlabel="Time Delay (ns)")
ax.legend(loc='upper left')
plt.grid(True)
fig.savefig('plots/wave_speed.png')
fig.show()
