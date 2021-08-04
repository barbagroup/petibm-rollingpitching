"""Plot the mesh grid."""

import itertools
import pathlib

import numpy
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial import ConvexHull

import petibmpy
import rodney


def subset_gridline(x, xs, xe):
    """Return subset of gridline points given a target start and end."""
    mask, = numpy.where((x >= xs) & (x <= xe))
    x = x[mask]
    xlim = (min(x), max(x))
    return x, xlim


args = rodney.parse_command_line()
maindir = pathlib.Path(__file__).parents[1]
datadir = maindir / 'output'

# Load gridline coordinates from file.
filepath = datadir / 'grid.h5'
x, y, z = petibmpy.read_grid_hdf5(filepath, 'vertex')

# Subset gridline coordinates.
x, xlim = subset_gridline(x, -5.0, 5.0)
y, ylim = subset_gridline(y, -5.0, 5.0)
z, zlim = subset_gridline(z, -5.0, 5.0)

# Load body coordinates from file.
filepath = maindir / 'wing.body'
wing = rodney.WingKinematics()
wing.load_body(filepath, skiprows=1)

# Keep only points on the contour of the wing.
x0, _, z0 = wing.get_coordinates(org=True)
points = numpy.array([x0, z0]).T
hull = ConvexHull(points)
x0, z0 = points[hull.vertices, 0], points[hull.vertices, 1]
y0 = numpy.zeros_like(x0)
wing.set_coordinates(x0, y0, z0, org=True)

# Get position at given time.
xb, yb, zb = wing.compute_position(0.0)

pyplot.rc('font', family='serif', size=12)

fig = pyplot.figure(figsize=(6.0, 6.0))
ax = Axes3D(fig, proj_type='persp')

ax.grid(False)
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False
ax.xaxis.pane.set_edgecolor('w')
ax.yaxis.pane.set_edgecolor('w')
ax.zaxis.pane.set_edgecolor('w')

ax.set_xlabel('x / c', labelpad=-10.0)
ax.set_ylabel('z / c', labelpad=-10.0)
ax.set_zlabel('y / c', labelpad=-10.0)

# Draw surrounding box.
lx, ly, lz = xlim[1] - xlim[0], ylim[1] - ylim[0], zlim[1] - zlim[0]
points = numpy.array(list(itertools.product(xlim, zlim, ylim)))
for s, e in itertools.combinations(points, 2):
    v = numpy.sum(numpy.abs(s - e))
    if v == lx or v == ly or v == lz:
        ax.plot3D(*zip(s, e), color='black', linestyle=':')

# Plot x/y gridlines at z_min.
X, Y = numpy.meshgrid(x, y)
Z = numpy.array([[min(z)]])
ax.plot_wireframe(X, Z, Y,
                  rstride=1, cstride=1, linewidth=0.1, color='black')

# Plot y/z gridlines at x_min.
Y, Z = numpy.meshgrid(y, z)
X = numpy.array([[min(x)]])
ax.plot_wireframe(X, Z, Y,
                  rstride=1, cstride=1, linewidth=0.1, color='black')

# Plot x/z gridlines at y_min
Z, X = numpy.meshgrid(z, x)
Y = numpy.array([[min(y)]])
ax.plot_wireframe(X, Z, Y,
                  rstride=1, cstride=1, linewidth=0.1, color='black')

# Plot wing.
ax.plot_trisurf(xb, zb, yb, color='C0')
# Add hinge.
ax.scatter(0.0, 0.0, 0.0, depthshade=False, c='black', marker='x', s=50)

ax.set_xlim3d(xlim)
ax.set_ylim3d(zlim[::-1])
ax.set_zlim3d(ylim)

ticks = numpy.arange(-5.0, 5.1, 2.5)
ax.set_xticks(ticks)
ax.set_xticklabels([None] * ticks.size)
ax.set_yticks(ticks)
ax.set_yticklabels([None] * ticks.size)
ax.set_zticks(ticks)
ax.set_zticklabels([None] * ticks.size)

if args.save_figures:
    figdir = maindir / 'figures'
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'meshgrid.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if args.show_figures:
    pyplot.show()
