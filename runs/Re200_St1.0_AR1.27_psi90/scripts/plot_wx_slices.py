"""Plot the 2D filled contours of the streamwise vorticity.

Slices of the 3D fields are shown in the "near" and "far" wakes
at non-dimensional time-unit 4.25.
The "near"-wake slice is chosen to be x=0.3.
The "far"-wake slice is chosen to be x=1.3.
"""

from matplotlib import pyplot, patches
import numpy
import pathlib
from string import ascii_lowercase

import petibmpy

import rodney


args = rodney.parse_command_line()
config = rodney.WingKinematics(Re=200, St=1.0, nt_period=2000)
simudir = pathlib.Path(__file__).absolute().parents[1]
datadir = simudir / 'output'
name = 'wx'  # name of the field to load
t_nodim = 4.25  # non-dimensional time
t = t_nodim * config.T  # time
timestep = int(t / config.dt)  # time-step index
theta = config.pitching(t)  # pitching angle (radians)

# Load the gridline coordinates from file.
filepath = datadir / 'grid.h5'
x, y, z = petibmpy.read_grid_hdf5(filepath, name)

# Load the field solution from file.
filepath = datadir / '{:0>7}.h5'.format(timestep)
wx = petibmpy.read_field_hdf5(filepath, name)
wx = numpy.moveaxis(wx, -1, 0)

if args.save_figures:
    figdir = simudir / 'figures'
    figdir.mkdir(parents=True, exist_ok=True)

xlocs = [0.0, 0.2, 0.3, 0.75, 1.1, 1.3, 1.85, 2.0, 2.7, 3.8, 4.5, 5.25]
alphabet = iter(ascii_lowercase)
pyplot.rc('font', family='serif', size=14)
for xloc in xlocs:
    fig, ax = pyplot.subplots(figsize=(6.0, 6.0))
    contourf_levels = numpy.linspace(-5.0, 5.0, num=50)
    contour_levels = numpy.linspace(-5.0, 5.0, num=10)
    wx_xloc = petibmpy.linear_interpolation(wx, x, xloc)
    ax.set_xlabel('z/c')
    ax.set_ylabel('y/c')
    ax.add_patch(patches.Ellipse((0.0, 0.0),
                                 config.S, config.c * numpy.sin(theta),
                                 edgecolor='black', facecolor='grey',
                                 alpha=0.5))
    ax.contourf(z - config.S / 2, y, wx_xloc.T,
                levels=contourf_levels, extend='both', cmap='viridis')
    ax.contour(z - config.S / 2, y, wx_xloc.T,
               levels=contour_levels, linewidths=0.5, colors='k')
    ax.axis('scaled', adjustable='box')
    ax.set_xlim(-1.25, 1.25)
    ax.set_ylim(-2.5, 2.5)
    fig.tight_layout()
    if args.save_figures:
        filepath = figdir / 'wx_slice_{}.png'.format(next(alphabet))
        fig.savefig(filepath, dpi=300, bbox_inches='tight')
