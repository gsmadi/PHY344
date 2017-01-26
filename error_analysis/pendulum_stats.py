import pandas as pd
import math

# Read time values
values = pd.read_csv('pendulum_ten_oscillations.csv', header=None,
                     names=['Time to oscillation'], nrows=10)

# Time measurement statistics
print values.describe()
# Time standard deviation of the mean
print 'Standard deviation of mean: ' + \
    str(values.std() / math.sqrt(len(values.index)))
