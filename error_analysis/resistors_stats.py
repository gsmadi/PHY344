import pandas as pd
import matplotlib.pyplot as plt
import math

# Read resistor values
values = pd.read_csv('resistors.csv', header=None,
                     names=['Resistance'], nrows=50)

# Plot histogram
values.plot.hist(by='Resistances', bins=30)

# Resistor measurement statistics
print values.describe()
# Resistor standard deviation of the mean
print 'Standard deviation of mean: ' + \
    str(values.std() / math.sqrt(len(values.index)))

plt.title('Resistor value histogram')
plt.xlabel('Measured resistor values')
plt.ylabel('Frequency')
plt.show()
