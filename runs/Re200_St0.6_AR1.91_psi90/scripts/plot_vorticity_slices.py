"""Plot the 2D contours of the streamwise and spanwise vorticity.

Solution is loaded from file at time value t/T = 4.25.
Slice the streamwise vorticity in the y/z plane in the near wake (x=0.3c).
Slice the spanwise vorticity in the x/y plane at the midspan (z=S/2).

"""

import collections
from matplotlib import pyplot, patches
import numpy
import pathlib

import petibmpy

import rodney


# Parse command line, and set kinematics and directories.
args = rodney.parse_command_line()
config = rodney.WingKinematics(Re=200, St=0.6, AR=1.91, nt_period=2000)
simudir = pathlib.Path(__file__).absolute().parents[1]
datadir = simudir / 'output'

# Set parameters.
t_nodim = 4.25  # non-dimensional time
t = t_nodim * config.T  # time
timestep = int(t / config.dt)  # time-step index
theta = config.pitching(t)  # pitching angle (radians)

if args.save_figures:
    # Create directory for figures if needed.
    figdir = simudir / 'figures'
    figdir.mkdir(parents=True, exist_ok=True)

# Set default font family and size for Matplotlib figures.
pyplot.rc('font', family='serif', size=14)

# Set number of levels for the contours.
contourf_levels = numpy.linspace(-5.0, 5.0, num=50)
contour_levels = numpy.linspace(-5.0, 5.0, num=10)

# Create data type to store information about annotation.
Annotation = collections.namedtuple('Annotation',
                                    ['text', 'xytext', 'xyarrow'])

# ----------------------------------------------------------------------------
# Plot the 2D slice of the streamwise vorticity in the y/z plane at x/c = 0.3.
# ----------------------------------------------------------------------------

# Load the gridline coordinates from file.
filepath = datadir / 'grid.h5'
x, y, z = petibmpy.read_grid_hdf5(filepath, 'wx')

# Load the field solution from file.
filepath = datadir / '{:0>7}.h5'.format(timestep)
wx = petibmpy.read_field_hdf5(filepath, 'wx')

# Interpolate the vorticity component in the y/z plane in the near wake.
xloc = 0.3  # location along the x direction (near wake)
wx_tmp = numpy.swapaxes(wx, -1, 0)
wx_xloc = petibmpy.linear_interpolation(wx_tmp, x, xloc)

# Create the Matplotlib figure.
fig, ax = pyplot.subplots(figsize=(4.0, 4.0))
ax.set_xlabel('z/c')
ax.set_ylabel('y/c')

# Add wing to the plot.
ax.add_patch(patches.Ellipse((0.0, 0.0),
                             config.S, config.c * numpy.sin(theta),
                             edgecolor='C0', linewidth=3.0, facecolor='gray',
                             alpha=0.5))
# Add contours of the vorticity component.
ax.contourf(z - config.S / 2, y, wx_xloc,
            levels=contourf_levels, extend='both', cmap='viridis')
ax.contour(z - config.S / 2, y, wx_xloc,
           levels=contour_levels, linewidths=0.5, colors='k')

# Set configuration of annotations to add.
annots = [Annotation('$V_1$', (-0.8, 0.4), (-0.77, 0.00)),
          Annotation('$V_2$', (0.6, -1.8), (0.42, -1.27)),
          Annotation('$V_3$', (-0.8, -1.0), (-0.52, -0.31)),
          Annotation('$V_4$', (0.6, 0.4), (0.71, -0.28))]
# Add annotations to figure.
for annot in annots:
    ax.annotate(annot.text, xy=annot.xyarrow, xycoords='data',
                xytext=annot.xytext,
                arrowprops=dict(facecolor='black', arrowstyle='-|>',
                                shrinkA=0, shrinkB=0))

# Set axes limits.
ax.axis('scaled', adjustable='box')
ax.axis((-1.0, 1.0, -2.0, 2.0))
fig.tight_layout()

if args.save_figures:
    filepath = figdir / f'wx_slice_yz_{timestep:0>7}.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

# ------------------------------------------------------------------------
# Plot the 2D slice of the spanwise vorticity in the x/y plane at z = S/2.
# ------------------------------------------------------------------------

# Load the gridline coordinates from file.
filepath = datadir / 'grid.h5'
x, y, z = petibmpy.read_grid_hdf5(filepath, 'wz')

# Load the field solution from file.
filepath = datadir / '{:0>7}.h5'.format(timestep)
wz = petibmpy.read_field_hdf5(filepath, 'wz')

# Interpolate the vorticity component in the x/y plane at midspan.
zloc = config.S / 2  # location along the z direction (midspan)
wz_zloc = petibmpy.linear_interpolation(wz, z, zloc)

# Create the Matplotlib figure.
fig, ax = pyplot.subplots(figsize=(4.0, 4.0))
ax.set_xlabel('x/c')
ax.set_ylabel('y/c')

# Add wing to the plot.
r = config.c / 2
xb = [-r * numpy.cos(theta), +r * numpy.cos(theta)]
yb = [+r * numpy.sin(theta), -r * numpy.sin(theta)]
ax.plot(xb, yb, color='C0', linewidth=3.0)

# Add contours of the vorticity component.
ax.contourf(x, y, wz_zloc,
            levels=contourf_levels, extend='both', cmap='viridis')
ax.contour(x, y, wz_zloc,
           levels=contour_levels, linewidths=0.5, colors='k')

# Set configuration of annotations to add.
annots = [Annotation('inner', (-0.3, -1.5), (0.70, -1.06)),
          Annotation('outer', (1.3, -1.5), (1.50, -0.80))]
# Add annotations to figure.
for annot in annots:
    ax.annotate(annot.text, xy=annot.xyarrow, xycoords='data',
                xytext=annot.xytext,
                arrowprops=dict(facecolor='black', arrowstyle='-|>',
                                shrinkA=0, shrinkB=0))

# Set axes limits.
ax.axis('scaled', adjustable='box')
ax.axis((-1.0, 3.0, -2.0, 2.0))
fig.tight_layout()

if args.save_figures:
    filepath = figdir / f'wz_slice_xy_{timestep:0>7}.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if args.show_figures:
    pyplot.show()
