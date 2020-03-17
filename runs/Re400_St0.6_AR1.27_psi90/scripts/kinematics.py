"""Fluid properties, geometric and kinematic parameters."""

import numpy


# Wing parameters.
c = 1.0  # chord length
AR = 1.27  # aspect ratio (AR = 1.27 --> S / c = 1)
S = numpy.pi * c * AR / 4  # span
A_plan = numpy.pi * c * S / 4  # planform area of the plate
R_avg = S / 2  # average rotational radius
CoR = [0.0, 0.0, 0.0]

# Fluid properties.
U_inf = 1.0  # freestream velocity
Re = 400.0  # Reynolds number
nu = U_inf * c / Re  # kinematic viscosity
rho = 1.0  # density

# Rolling parameters.
A_phi = numpy.radians(45.0)  # rolling amplitude

# Pitching parameters.
A_theta = numpy.radians(45.0)  # pitching amplitude
psi = numpy.radians(90.0)  # phase difference
theta_bias = numpy.radians(0.0)  # static pitching bias

# Temporal parameters.
St = 0.6  # Strouhal number
f = St * U_inf / (2 * A_phi * R_avg)  # flapping frequency
T = 1 / f  # time period

# Simulation parameters.
n_periods = 5  # number of periods
tf = n_periods * T  # final time
nt_period = 2000  # number of time steps per period
nt = n_periods * nt_period  # number of time steps
dt = tf / nt  # time-step size


if __name__ == '__main__':
    print(locals())
