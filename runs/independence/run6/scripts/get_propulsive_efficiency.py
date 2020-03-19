"""Compute the hydrodynamic power and propulsive efficiency."""

import h5py
import numpy
import pathlib

import petibmpy

import rodney


def load_probe_solution(filepath, t, field):
    return petibmpy.ProbeVolume(field, field).read_hdf5(filepath, t)

def get_index_neighbors(points, grid):
    xp, yp, zp = points
    x, y, z = grid
    # Bottom-left neighbors.
    i = numpy.searchsorted(x, xp) - 1
    j = numpy.searchsorted(y, yp) - 1
    k = numpy.searchsorted(z, zp) - 1
    return i, j, k


def trilinear_interpolation(x, y, z, p0, p1, v):
    x0, y0, z0 = p0
    x1, y1, z1 = p1
    c000, c001, c010, c011, c100, c101, c110, c111 = v
    xd = (x - x0) / (x1 - x0)
    yd = (y - y0) / (y1 - y0)
    zd = (z - z0) / (z1 - z0)
    c00 = c000 * (1 - xd) + c100 * xd
    c01 = c001 * (1 - xd) + c101 * xd
    c10 = c010 * (1 - xd) + c110 * xd
    c11 = c011 * (1 - xd) + c111 * xd
    c0 = c00 * (1 - yd) + c10 * yd
    c1 = c01 * (1 - yd) + c11 * yd
    return c0 * (1 - zd) + c1 * zd


def interpolate_pressure(x, y, z, t, datadir):
    num_points = x.size
    filepath = datadir / 'probe_vicinity-p.h5'
    grid, p = load_probe_solution(filepath, t, 'p')
    i_all, j_all, k_all = get_index_neighbors((x, y, z), grid)
    xp, yp, zp = grid
    p_interp = numpy.empty(num_points)
    for l in range(num_points):
        point = (x[l], y[l], z[l])
        i, j, k = k_all[l], j_all[l], i_all[l]
        p0 = (xp[i], yp[j], zp[k])
        p1 = (xp[i + 1], yp[j + 1], zp[k + 1])

        c000 = p[k, j, i]
        c001 = p[k, j + 1, i]
        c010 = p[k + 1, j, i]
        c011 = p[k + 1, j + 1, i]
        c100 = p[k, j, i + 1]
        c101 = p[k, j + 1, i + 1]
        c110 = p[k + 1, j, i + 1]
        c111 = p[k + 1, j + 1, i + 1]
        v = (c000, c001, c010, c011, c100, c101, c110, c111)
        p_interp[l] = trilinear_interpolation(*point, p0, p1, v)
    return p_interp


def compute_hydrodynamic_power(p, n, u, ds):
    return -numpy.sum(p * numpy.sum(numpy.multiply(n, u), axis=1) * ds)


class Point(object):
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z

    def asarray(self):
        arr = numpy.array([self.x, self.y, self.z])
        if arr.ndim == 2:
            return arr.T
        return arr


def get_normal(p1, p2, p3):
    v1 = (p1 - p2) / numpy.linalg.norm(p1 - p2)
    v2 = (p3 - p1) / numpy.linalg.norm(p3 - p1)
    v3 = numpy.cross(v1, v2)
    return v3 / numpy.linalg.norm(v3)


# Set simulation directory and data directory.
simudir = pathlib.Path(__file__).absolute().parents[1]
datadir = simudir / 'output'

# Create the wing kinematics.
wing = rodney.WingKinematics(Re=200.0, St=0.6, nt_period=2000)

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
x0, y0, z0 = wing.get_coordinates()
# Grab 3 reference points (to later compute unit normal vector).
points0 = Point(x0[:3], y0[:3], z0[:3])

dx = 0.01  # grid-spacing size in the vicinity of the body
ds = dx**2  # surface area associated with each marker

# Create virtual boundary around flat plate.
# The flat surface is extended by d grid cells on lower and upper surfaces.
d = 3 * dx  # normal distance from original markers
xv0 = numpy.tile(x0, 2)
yv0 = numpy.concatenate((y0 - d, y0 + d))
zv0 = numpy.tile(z0, 2)
# Replace flat surface with virtual body.
wing.set_coordinates(xv0, yv0, zv0, org=True)

# Read time values of probe recordings.
filepath = datadir / 'probe_vicinity-p.h5'
with h5py.File(filepath, 'r') as infile:
    times = [float(t_str) for t_str in list(infile['p'].keys())]

# Initialize array to contain hydrodynamic power for each time recording.
P_hydro = numpy.empty_like(times)

# Compute the hydrodynamic power over the time records.
for i, time in enumerate(times):
    print(f'[t/T = {time / wing.T:.6f}] Computing hydrodynamic power ...')

    # Get the rolling and pitching angles.
    phi = wing.rolling(time)
    theta = wing.pitching(time)
    # Rotate the reference points (to next compute the unit normal).
    points = Point(*rodney.vrotation(points0.x, points0.y, points0.z,
                                     roll=phi, pitch=theta, center=wing.hook))
    # Compute the unit normal vector.
    n = get_normal(*points.asarray())

    # Update the position and velocity of the body.
    wing.update_position(time)

    # Interpolate the pressure on the virtual boundary.
    p = interpolate_pressure(*wing.get_coordinates(), time, datadir)

    # Get the normal for each marker on the virtual boundary.
    n = numpy.concatenate((numpy.tile(-n, (wing.size // 2, 1)),
                           numpy.tile(+n, (wing.size // 2, 1))))

    # Compute the body velocity and gather components.
    wing.update_velocity(time)
    u = numpy.vstack(wing.get_velocity()).T

    # Compute the hydrodynamic power.
    P_hydro[i] = compute_hydrodynamic_power(p, n, u, ds)

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
