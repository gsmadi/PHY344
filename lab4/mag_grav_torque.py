import matplotlib.pyplot as plt
import numpy as np

m = 1.3E-3
g = 9.8  # [m*s^2]

b_field = np.array([0.00375, 0.00405, 0.00435, 0.00465, 0.00495,
                    0.00510, 0.00555, 0.00570, 0.0060])

r = np.array([6.7, 7.8, 8.7, 10.2, 10.6, 11.4, 12.3, 12.8, 14.0])

coefficients, residuals = np.polyfit(b_field, r, deg=1, cov=True)

slope = coefficients[0]*1E-2
intercept = coefficients[1]*1E-2

slope_uncertainty = np.sqrt(residuals[0][0])*1E-2
intercept_uncertainty = np.sqrt(residuals[1][1])*1E-2

mu = m*g*slope
delta_mu = 0.1

print "Slope: {} +/- {}".format(slope, slope_uncertainty)
print "Intercept: {} +/- {}".format(intercept, intercept_uncertainty)
print "\n\nmu = {} +/- {}".format(mu, )
