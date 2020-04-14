"""Compute the hydrodynamic power and propulsive efficiency."""

import h5py
import numpy
import pathlib
from scipy.interpolate import RegularGridInterpolator

import petibmpy

import rodney


def load_probe_solution(filepath, t, field):
    return petibmpy.ProbeVolume(field, field).read_hdf5(filepath, t)


def load_time_values_hdf5(filepath, name='p'):
    with h5py.File(filepath, 'r') as infile:
        times = [float(t_str) for t_str in list(infile[name].keys())]
    return times


def compute_hydrodynamic_power(p, n, u, ds):
    return numpy.sum(p * numpy.sum(numpy.multiply(n, u), axis=1) * ds)


def wing_get_normal(wing, time):
    phi = wing.rolling(time)
    theta = wing.pitching(time)
    points = numpy.array([[0.0, 0.0, 0.0],
                          [0.5, 0.0, 0.5],
                          [-0.5, 0.0, 0.5]]).T
    x, y, z = rodney.vrotation(*points,
                               roll=phi, pitch=theta,
                               center=wing.hook)
    p1, p2, p3 = numpy.array([x, y, z]).T

    v1 = (p1 - p2) / numpy.linalg.norm(p1 - p2)
    v2 = (p3 - p1) / numpy.linalg.norm(p3 - p1)
    v3 = numpy.cross(v1, v2)
    return v3 / numpy.linalg.norm(v3)


# Set simulation directory and data directory.
simudir = pathlib.Path(__file__).absolute().parents[1]
datadir = simudir / 'output'

# Create the wing kinematics.
wing = rodney.WingKinematics(Re=200.0, St=0.8, nt_period=2000)

# Compute the cycle-averaged thrust.
filepath = datadir / 'forces-0.txt'
t, fx, _, _ = petibmpy.read_forces(filepath)
thrust = -fx  # switch from drag to thrust
time_limits = (4 * wing.T, 5 * wing.T)  # interval to consider for average
thrust_avg, = petibmpy.get_time_averaged_values(t, thrust, limits=time_limits)

# Compute the cycle-averaged thrust coefficient.
rho, U_inf, A_plan = (getattr(wing, name)
                      for name in ('rho', 'U_inf', 'A_plan'))
scale = 1 / (0.5 * rho * U_inf**2 * A_plan)
ct, = petibmpy.get_force_coefficients(thrust, coeff=scale)
ct_avg, = petibmpy.get_time_averaged_values(t, ct, limits=time_limits)

# Load original boundary coordinates from file.
filepath = simudir / 'wing.body'
wing.load_body(filepath, skiprows=1)

# Compute surface area associated with each Lagrangian marker.
ds = wing.A_plan / wing.size

# Create virtual boundary around flat plate.
# The flat surface is extended by d grid cells on lower and upper surfaces.
d = 0.03 * wing.c  # normal distance from original markers (3% chord length)
x0, y0, z0 = wing.get_coordinates()
xv0 = numpy.tile(x0, 2)
yv0 = numpy.concatenate((y0 - d, y0 + d))
zv0 = numpy.tile(z0, 2)
# Replace flat surface with virtual body.
wing.set_coordinates(xv0, yv0, zv0, org=True)

# Read time values of probe recordings.
filepath = datadir / 'probe_vicinity-p.h5'
times = load_time_values_hdf5(filepath)

# Create regular-grid interpolator.
grid, p = load_probe_solution(filepath, times[0], 'p')
interpolator = RegularGridInterpolator(grid, p.T)

# Initialize array to contain hydrodynamic power for each time recording.
P_hydro = numpy.empty_like(times)

# Compute the hydrodynamic power over the time records.
for i, time in enumerate(times):
    print(f'[t/T = {time / wing.T:.6f}] Computing hydrodynamic power ...')

    # Compute the unit normal vector.
    n = wing_get_normal(wing, time)

    # Update the position and velocity of the body.
    wing.update_position(time)

    # Update pressure data on regular grid.
    _, p = load_probe_solution(filepath, time, 'p')
    interpolator.values = p.T

    # Interpolate the pressure on the virtual boundary.
    xi, yi, zi = wing.get_coordinates()
    p = interpolator(numpy.array([xi, yi, zi]).T)

    # Get the normal for each marker on the virtual boundary.
    n = numpy.concatenate((numpy.tile(-n, (wing.size // 2, 1)),
                           numpy.tile(+n, (wing.size // 2, 1))))

    # Compute the body velocity and gather components.
    wing.update_velocity(time)
    u = numpy.vstack(wing.get_velocity()).T

    # Compute the hydrodynamic power.
    P_hydro[i] = compute_hydrodynamic_power(p, n, u, ds)

# Save hydrodynamic power over cycle to file.
filepath = datadir / 'P_hydro.dat'
with open(filepath, 'w') as outfile:
    numpy.savetxt(outfile, numpy.c_[times, P_hydro])

# Compute the cycle-averaged hydrdynamic power.
# As in Li & Dong (2016), only positive values are considered.
mask = numpy.where(P_hydro > 0.0)
P_hydro_avg = numpy.mean(P_hydro[mask])

# Compute the propulsive efficiency.
eta = thrust_avg * U_inf / P_hydro_avg

# Print data.
print('Cycle-averaged thrust:', thrust_avg)
print('Cycle-averaged thrust coefficient:', ct_avg)
print('Cycle-averaged hydrodynamic power:', P_hydro_avg)
print('Propulsive efficiency:', eta)
