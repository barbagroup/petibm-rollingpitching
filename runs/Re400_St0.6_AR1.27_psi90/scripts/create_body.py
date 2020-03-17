"""Create the body and write the coordinates to a file."""

import distmesh
import numpy
import pathlib

import petibmpy

from kinematics import c, AR, CoR, S


# Set the simulation directory.
simudir = pathlib.Path(__file__).absolute().parents[1]

# Create distance function.
a, b = c / 2, S / 2
xc, yc, zc = CoR[0], CoR[1], CoR[2] + b


def fd(p):
    """Distance function."""
    return (p[:, 0] - xc)**2 / a**2 + (p[:, 1] - zc)**2 / b**2 - 1


# Discretize the ellipse.
ds = 0.01 * c  # mesh resolution
bbox = (xc - a, zc - b, xc + a, zc + b)  # bounding box
p, t = distmesh.distmesh2d(fd, distmesh.huniform, ds, bbox, fig=None)

# Store the coordinates in arrays.
x0, z0 = p[:, 0], p[:, 1]
y0 = numpy.zeros_like(x0)

sort_points = True
if sort_points:
    idx = numpy.argmin(z0)
    xp, zp = x0[idx], z0[idx]
    dist = numpy.sqrt((x0 - xp)**2 + (z0 - zp)**2)
    indices = numpy.argsort(dist)
    x0, z0 = x0[indices], z0[indices]

# Save the coordinates into a file.
filepath = simudir / 'wing.body'
petibmpy.write_body(filepath, x0, y0, z0)
