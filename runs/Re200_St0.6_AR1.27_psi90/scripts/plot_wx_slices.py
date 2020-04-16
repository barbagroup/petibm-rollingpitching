"""Plot the 2D slices of the streamwise vorticity at locations in the wake."""

import collections
from matplotlib import pyplot, patches
import numpy
import pathlib
from string import ascii_lowercase
import yaml

import petibmpy

import rodney


# Parse command line and set directories.
args = rodney.parse_command_line()
simudir = pathlib.Path(__file__).absolute().parents[1]
datadir = simudir / 'output'

# Set configuration of the wing kinematics.
config = rodney.WingKinematics(Re=200, St=0.6, nt_period=2000)

# Set parameters.
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
    # Create directory if not already existing.
    figdir = simudir / 'figures'
    figdir.mkdir(parents=True, exist_ok=True)

# Locations to consider along the x direction.
xlocs = [0.0, 0.2, 0.3, 0.75, 1.1, 1.3, 1.85, 2.0, 2.7, 3.8, 4.5, 5.25]

# Change default font family and size for Matplotlib figures.
pyplot.rc('font', family='serif', size=10)

# Will use letters to define slices.
alphabet = iter(ascii_lowercase)

# Set axes limits and size of the Matplotlib figures to create.
Box = collections.namedtuple('Box', ['xs', 'xe', 'ys', 'ye'])
box = Box(-1.25, 1.25, -2.5, 2.5)
width, height = box.xe - box.xs, box.ye - box.ys
scale = 2.0
figsize = (width / scale, height / scale)

if args.extra_data:
    # Load information about the text annotations to add to figures.
    filepath = pathlib.Path(__file__).parent / 'wx_slices_annotations.yaml'
    with open(filepath, 'r') as infile:
        annot = yaml.safe_load(infile)['xlocs']

# Loop over the slices to compute and plot.
for xloc in xlocs:
    print(f'[xloc = {xloc}] Computing and plotting wx slice ...')

    # Initialize figure.
    fig = pyplot.figure(figsize=(width / scale, height / scale),
                        dpi=300, frameon=False)
    ax = pyplot.Axes(fig, [0.0, 0.0, 1.0, 1.0])

    # Interpolate the 3D vorticity compenent at given x location.
    wx_xloc = petibmpy.linear_interpolation(wx, x, xloc)

    # Represent the wing on the figure.
    ax.add_patch(patches.Ellipse((0.0, 0.0),
                                 config.S, config.c * numpy.sin(theta),
                                 edgecolor='black', facecolor='gray',
                                 alpha=0.5))

    # Add the contours of the vorticity component.
    contourf_levels = numpy.linspace(-5.0, 5.0, num=50)
    contour_levels = numpy.linspace(-5.0, 5.0, num=10)
    ax.contourf(z - config.S / 2, y, wx_xloc.T,
                levels=contourf_levels, extend='both', cmap='viridis')
    ax.contour(z - config.S / 2, y, wx_xloc.T,
               levels=contour_levels, linewidths=0.25, colors='black')

    if args.extra_data:
        # Add text annotations and arrows.
        if xloc in annot.keys():
            for elem in annot[xloc]:
                text, xytext = elem['text'], elem['xytext']
                xyarrow = elem.get('xyarrow', None)
                if xyarrow is None:
                    ax.annotate(text, xy=xytext, xycoords='data')
                else:
                    ax.annotate(text, xy=xyarrow, xycoords='data',
                                xytext=xytext,
                                arrowprops=dict(facecolor='black',
                                                linewidth=0.5,
                                                arrowstyle='-|>',
                                                shrinkA=0, shrinkB=0))

    # Finialize figure.
    ax.axis('scaled', adjustable='box')
    ax.set_xlim(box.xs, box.xe)
    ax.set_ylim(box.ys, box.ye)
    ax.axis('off')
    fig.add_axes(ax)
    if args.save_figures:
        # Save the figure.
        filepath = figdir / 'wx_slice_{}.png'.format(next(alphabet))
        fig.savefig(filepath, dpi=300, bbox_inches='tight')
