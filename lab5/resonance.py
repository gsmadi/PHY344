
import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import optimize
import statsmodels.api as sm

omega_naught = 3.29

damping_rates = np.array([0.07, 0.10, 0.18, 0.25])
