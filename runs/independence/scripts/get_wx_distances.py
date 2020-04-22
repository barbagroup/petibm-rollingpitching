"""Measure the distances between the inner and outer vortex pairs.

We take a slice of the streamwise vorticity at x = 0.3 and x = 1.3
at non-dimensional time unit 4.25.

The center of each vortex is chosen as the point witht the (absolute)
highest value of the streamwise value.

"""

import collections
from matplotlib import pyplot, patches
import numpy
import pathlib

import petibmpy

import rodney


Point2D = collections.namedtuple('Point2D', ['x', 'y'])
Box2D = collections.namedtuple('Box2D', ['xs', 'xe', 'ys', 'ye'])


def load_field_3d(datadir, config, time, name):
    # Set parameters.
    time *= config.T  # convert to dimensional time
    timestep = int(time / config.dt)  # time-step index
    # Load gridline coordinates from file.
    filepath = datadir / 'grid.h5'
    x, y, z = petibmpy.read_grid_hdf5(filepath, name)
    # Shift z locations to match figures of Li & Dong (2016).
    z -= config.S / 2
    # Load 3D field solution from file.
    filepath = datadir / f'{timestep:0>7}.h5'
    field = petibmpy.read_field_hdf5(filepath, name)
    # Return grid and streamwise vorticity.
    return (x, y, z), field


def get_field_slices_2d(grid, field, xlocs):
    x, y, z = grid
    # Interpolate field at given x-locations.
    field_slices = []
    field = numpy.swapaxes(field, 0, -1)  # swap z and x axes
    for xloc in xlocs:
        field_slice = petibmpy.linear_interpolation(field, x, xloc)
        field_slices.append(field_slice)
    # Return the y and z gridline coordinates
    # and the slices of the field solution.
    return (y, z), field_slices


def get_field_in_box_2d(grid, field, box):
    x, y = grid
    # Get starting and ending indices for the box.
    i_s = numpy.searchsorted(x, box.xs)
    i_e = numpy.searchsorted(x, box.xe)
    j_s = numpy.searchsorted(y, box.ys)
    j_e = numpy.searchsorted(y, box.ye)
    # Get solution in box.
    x, y = x[i_s:i_e], y[j_s:j_e]
    field = field[j_s:j_e, i_s:i_e]
    return (x, y), field


def get_extreme_points_2d(grid, field):
    indices = numpy.argsort(field.flatten())
    x, y = grid
    lda = x.size
    I = indices[0]
    min_point = Point2D(x[I % lda], y[I // lda])
    I = indices[-1]
    max_point = Point2D(x[I % lda], y[I // lda])
    return {'min': min_point, 'max': max_point}


def plot_wx_slice_2d(grid, wx, time, config):
    pyplot.rc('font', family='serif', size=14)
    fig, ax = pyplot.subplots(figsize=(6.0, 6.0))
    contourf_levels = numpy.linspace(-5.0, 5.0, num=50)
    contour_levels = numpy.linspace(-5.0, 5.0, num=10)
    ax.set_xlabel('z/c')
    ax.set_ylabel('y/c')
    # Add patch to represent the wing.
    c, S = config.c, config.S
    theta = config.pitching(time * config.T)
    ax.add_patch(patches.Ellipse((0.0, 0.0), S, c * numpy.sin(theta),
                                 edgecolor='black', facecolor='gray',
                                 alpha=0.5))
    # Add filled contour of the streamwise vorticity.
    ax.contourf(*grid, wx,
                levels=contourf_levels, extend='both', cmap='viridis')
    # Add contours of the streamwise vorticity.
    ax.contour(*grid, wx,
               levels=contour_levels, linewidths=0.5, colors='k')
    # Finalize figure.
    ax.axis('scaled', adjustable='box')
    ax.set_xlim(-1.0, 1.0)
    ax.set_ylim(-2.0, 2.0)
    fig.tight_layout()
    return fig, ax


def add_annotations(ax, p1, p2, y, text=''):
    # Add markers to visualize points.
    ax.scatter([p1.x, p2.x], [p1.y, p2.y], c='C0', s=20, marker='o')
    # Add vertical lines from points to y.
    ax.vlines(p1.x, y, p1.y, color='black', linestyle='--')
    ax.vlines(p2.x, y, p2.y, color='black', linestyle='--')
    # Add two-head arrow between vertical lines.
    ax.annotate('', xy=(p2.x, y), xytext=(p1.x, y),
                arrowprops=dict(arrowstyle='<->', shrinkA=0.0, shrinkB=0.0))
    # Add text description above arrow.
    ax.annotate(text, xy=(0.5 * (p1.x + p2.x), y + 0.1))


def get_wx_distances(simudir, config, plot=False, save_figures=False):
    time = 4.25  # non-dimensional time value
    datadir = simudir / 'output'
    grid, wx = load_field_3d(datadir, config, time, 'wx')
    xlocs = [0.3, 1.3]
    (y, z), wx_slices = get_field_slices_2d(grid, wx, xlocs)

    box1 = Box2D(-0.6, -0.4, -0.4, 0.1)
    g1, s1 = get_field_in_box_2d((z, y), wx_slices[0], box1)
    p1 = get_extreme_points_2d(g1, s1)['max']

    box2 = Box2D(0.1, 0.5, -1.0, -0.6)
    g2, s2 = get_field_in_box_2d((z, y), wx_slices[0], box2)
    p2 = get_extreme_points_2d(g2, s2)['min']

    box3 = Box2D(-0.5, 0.4, -0.35, -0.1)
    g3, s3 = get_field_in_box_2d((z, y), wx_slices[0], box3)
    p3 = get_extreme_points_2d(g3, s3)['min']

    box4 = Box2D(0.0, 0.5, -0.8, -0.2)
    g4, s4 = get_field_in_box_2d((z, y), wx_slices[0], box4)
    p4 = get_extreme_points_2d(g4, s4)['max']

    if plot:
        fig1, ax1 = plot_wx_slice_2d((z, y), wx_slices[0], time, config)
        add_annotations(ax1, p1, p2, -1.5, '$d_2$')
        add_annotations(ax1, p3, p4, +1.0, '$d_1$')

    box5 = Box2D(-0.6, -0.1, 0.3, 0.9)
    g5, s5 = get_field_in_box_2d((z, y), wx_slices[1], box5)
    p5 = get_extreme_points_2d(g5, s5)['min']

    box6 = Box2D(0.3, 0.8, 0.7, 1.3)
    g6, s6 = get_field_in_box_2d((z, y), wx_slices[1], box6)
    p6 = get_extreme_points_2d(g6, s6)['max']

    box7 = Box2D(-0.2, 0.2, 0.2, 0.9)
    g7, s7 = get_field_in_box_2d((z, y), wx_slices[1], box7)
    p7 = get_extreme_points_2d(g7, s7)['max']

    box8 = Box2D(0.1, 0.4, 0.25, 0.65)
    g8, s8 = get_field_in_box_2d((z, y), wx_slices[1], box8)
    p8 = get_extreme_points_2d(g8, s8)['min']

    if plot:
        fig2, ax2 = plot_wx_slice_2d((z, y), wx_slices[1], time, config)
        add_annotations(ax2, p5, p6, -1.0, '$d_4$')
        add_annotations(ax2, p7, p8, +1.5, '$d_3$')

    d1 = abs(p4.x - p1.x)
    d2 = abs(p3.x - p2.x)
    d3 = abs(p8.x - p7.x)
    d4 = abs(p6.x - p5.x)

    if plot:
        return (d1, d2, d3, d4), (fig1, ax1), (fig2, ax2)
    return d1, d2, d3, d4


args = rodney.parse_command_line()

# Set directories.
maindir = pathlib.Path(__file__).absolute().parents[1]

distances = {}

# Process solution on nominal grid.
label = 'Nominal'
simudir = maindir / 'run3'
config = rodney.WingKinematics(nt_period=2000)
dist, (fig1, ax1), (fig2, ax2) = get_wx_distances(simudir, config, plot=True)
distances[label] = dist
if args.save_figures:
    figdir = maindir / 'figures'
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'wx_slice_c_distances.png'
    fig1.savefig(filepath, dpi=300, bbox_inches='tight')
    filepath = figdir / 'wx_slice_f_distances.png'
    fig2.savefig(filepath, dpi=300, bbox_inches='tight')

# Process solution on finer grid in space.
label = 'Finer in space'
simudir = maindir / 'run4'
config = rodney.WingKinematics(nt_period=2000)
distances[label] = get_wx_distances(simudir, config)

# Process solution on coarser grid in time.
label = 'Coarser in time'
simudir = maindir / 'run6'
config = rodney.WingKinematics(nt_period=1000)
distances[label] = get_wx_distances(simudir, config)

# Print distances (Markdown format).
print('| Case | $d_1$ | $d_2$ | $d_3$ | $d_4$ |')
print('|:-:|:-:|:-:|:-:|:-:|')
for label, dist in distances.items():
    print('| {} | ${:.3f}$ | ${:.3f}$ | ${:.3f}$ | ${:.3f}$ |'
          .format(label, *dist))

pyplot.show()

