import pandas as pd
import matplotlib.pyplot as plt
import math

# Read resistor values
values = pd.read_csv('disk_data.csv', header=None,
                     names=['Circumference', 'Diameter'], nrows=5)

# Set error
xerrors = values.std()['Circumference']
yerrors = values.std()['Diameter']

# Plot graph
values.plot(x='Circumference', y='Diameter',
            marker='.', xerr=xerrors, yerr=yerrors)

# Resistor measurement statistics
print values.describe()
# Resistor standard deviation of the mean
print 'Standard deviation of mean: ' + \
    str(values.std() / math.sqrt(len(values.index)))

plt.title('Circumference vs. Diameter')
plt.xlabel('Circumference')
plt.ylabel('Diameter')
plt.show()
