import matplotlib.pyplot as plt
import pandas as pd

# Read data points
values = pd.read_csv('data/filter436.csv', header=None,
                     names=['Voltage', 'Current'],
                     nrows=20)


# Plot points
ax = values.plot(x='Voltage', y='Current', title="IV Curve",
            marker='o', markersize=2, grid='on', label="Filter 436nm",
            xlim=[values.min()['Voltage'], 4])

ax.set(xlabel="Voltage (V)", ylabel="Current (nA)")
fig = ax.get_figure()

fig.savefig('plots/filter436.png')
fig.show()
