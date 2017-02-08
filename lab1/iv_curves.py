import pandas as pd
import matplotlib.pyplot as plt

# Read resistor values
values = pd.read_csv('data/test_run.csv', header=None,
                     names=['Voltage', 'Current'],
                     nrows=20)

values.interpolate(method='cubic')

# Plot points
values.plot(x='Voltage', y='Current',
            marker='o', markersize=2, grid='on',
            label="No filter")


plt.title('IV Curve')
plt.xlim([values.min()['Voltage'], 3])
plt.xlabel('Voltage (V)')
plt.ylabel('Current (nA)')
plt.savefig('plots/test_run.png')
