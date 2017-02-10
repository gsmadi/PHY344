import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Read resistor values
values = pd.read_csv('data/disk_data.csv', header=None,
                     names=['Diameter', 'Circumference',
                            'Diameter Uncertainty',
                            'Circumference Uncertainty',
                            'Ratio', 'Ratio Uncertainty'],
                     nrows=5)
values.sort(['Circumference'], ascending=[True])
# Set error
xerrors = values.mean()['Circumference Uncertainty']
yerrors = values.mean()['Diameter Uncertainty']

# Plot points
values.plot(x='Circumference', y='Diameter',
            marker='o', markersize=4,
            elinewidth=4,
            xerr=xerrors,
            yerr=yerrors, grid='on',
            label="Circumference/Diameter",
            linestyle="--")

# Resistor measurement statistics
print values.describe()
# Resistor standard deviation of the mean
print 'Standard deviation of mean:'
print str(values.std() / math.sqrt(len(values.index)))

slope, intercept = np.polyfit(x=values['Circumference'], y=values['Diameter'],
                              deg=1)
print 'Slope of fitted line: ' + str(slope)

plt.title('Circumference vs. Diameter')
plt.xlim([18.2, 55.4])
plt.ylim([5.9, 17.5])
plt.xlabel('Circumference (cm)')
plt.ylabel('Diameter (cm)')
plt.show()
