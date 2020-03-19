"""Measure the distances between the inner and outer vortex pairs.

We take a slice of the streamwise vorticity at x = 0.3 and x = 1.3
at non-dimensional time unit 4.25.

The center of each vortex is chosen as the point witht the (absolute)
highest value of the streamwise value.

"""

from matplotlib import pyplot, patches
import numpy
import pathlib
from string import ascii_lowercase

import petibmpy

import rodney


def get_sub_area_2d(field, x, y, bottom_left, width, height):
    xlim = (bottom_left[0], bottom_left[0] + width)
    ylim = (bottom_left[1], bottom_left[1] + height)
    i = numpy.where((x >= xlim[0]) & (x <= xlim[1]))[0]
    ilim = (i[0], i[-1])
    j = numpy.where((y >= ylim[0]) & (y <= ylim[1]))[0]
    jlim = (j[0], j[-1])
    sub_field = field[jlim[0]:jlim[-1] + 1, ilim[0]:ilim[-1] + 1]
    sub_x, sub_y = x[i], y[j]
    return sub_field, (sub_x, sub_y)


def create_plot(wx, z, y):
    fig, ax = pyplot.subplots(figsize=(6.0, 6.0))
    contourf_levels = numpy.linspace(-5.0, 5.0, num=50)
    contour_levels = numpy.linspace(-5.0, 5.0, num=10)
    ax.set_xlabel('z/c')
    ax.set_ylabel('y/c')
    ax.add_patch(patches.Ellipse((0.0, 0.0), S, c * numpy.sin(theta),
                                 edgecolor='black', facecolor='grey',
                                 alpha=0.5))
    ax.contourf(z, y, wx,
                levels=contourf_levels, extend='both', cmap='viridis')
    ax.contour(z, y, wx,
               levels=contour_levels, linewidths=0.5, colors='k')
    ax.axis('scaled', adjustable='box')
    ax.set_xlim(-1.0, 1.0)
    ax.set_ylim(-2.0, 2.0)
    fig.tight_layout()
    return fig, ax


def get_extreme_values(wx, z, y, num=1):
    def get_coordinates(indices):
        lda = z.size
        z_ = numpy.array([z[I % lda] for I in indices])
        y_ = numpy.array([y[I // lda] for I in indices])
        return z_, y_
    indices = numpy.argsort(wx.flatten())
    min_indices, max_indices = indices[:num], indices[-num:]
    return {'min': get_coordinates(min_indices),
            'max': get_coordinates(max_indices)}


def add_extreme_values(ax, wx, z, y, box, config='min', num=1):
    bottom_left = (box[0][0], box[1][0])
    width, height = box[0][1] - box[0][0], box[1][1] - box[1][0]
    wx_sub, (z_sub, y_sub) = get_sub_area_2d(wx_xloc, z, y,
                                             bottom_left, width, height)
    rect = patches.Rectangle(bottom_left, width, height,
                             edgecolor='black', facecolor='none')
    ax.add_patch(rect)
    points = get_extreme_values(wx_sub, z_sub, y_sub, num=num)
    points = points[config]
    c = 'C0' if config == 'min' else 'C3'
    ax.scatter(points[0], points[1], c=c, s=20, marker='x')
    return points


# Set directories.
simudir = pathlib.Path(__file__).absolute().parents[1]
datadir = simudir / 'output'

# Set wing kinematics.
config = rodney.WingKinematics(nt_period=1000)
c = config.c  # chord length
S = config.S  # spanwise length
T = config.T  # period
dt = config.dt  # time-step size

name = 'wx'  # name of the field to load
t = 4.25 * T  # time
timestep = int(t / dt)  # time-step index
theta = config.pitching(t)  # pitching angle (radians)

# Load the gridline coordinates from file.
filepath = datadir / 'grid.h5'
x, y, z = petibmpy.read_grid_hdf5(filepath, name)
z -= S / 2  # shift z locations to match figures of Li & Dong (2016)

# Load the field solution from file.
filepath = datadir / '{:0>7}.h5'.format(timestep)
wx = petibmpy.read_field_hdf5(filepath, name)
wx = numpy.swapaxes(wx, 0, -1)

figdir = simudir / 'figures'
figdir.mkdir(parents=True, exist_ok=True)

pyplot.rc('font', family='serif', size=14)

wx_xloc = petibmpy.linear_interpolation(wx, x, 0.3)
fig, ax = create_plot(wx_xloc, z, y)
# Search for maximum in V1.
box = ((-0.6, -0.4), (-0.4, 0.1))
points = add_extreme_values(ax, wx_xloc, z, y, box, config='max', num=1)
z_V1, y_V1 = points[0][-1], points[1][-1]
print(f'V1: ({y_V1:.4f}, {z_V1:.4f})')
# Search for minimum in V2.
box = ((0.1, 0.5), (-1.0, -0.6))
points = add_extreme_values(ax, wx_xloc, z, y, box, config='min', num=1)
z_V2, y_V2 = points[0][0], points[1][0]
print(f'V2: ({y_V2:.4f}, {z_V2:.4f})')
# Search for minimum in V3.
box = ((-0.5, 0.4), (-0.35, -0.1))
points = add_extreme_values(ax, wx_xloc, z, y, box, config='min', num=1)
z_V3, y_V3 = points[0][0], points[1][0]
print(f'V3: ({y_V3:.4f}, {z_V3:.4f})')
# Search for maximum in V4.
box = ((0.0, 0.5), (-0.8, -0.2))
points = add_extreme_values(ax, wx_xloc, z, y, box, config='max', num=1)
z_V4, y_V4 = points[0][-1], points[1][-1]
print(f'V4: ({y_V4:.4f}, {z_V4:.4f})')

print(f'd1 = {abs(z_V3 - z_V4):.4f}')
print(f'd2 = {abs(z_V1 - z_V2):.4f}')

wx_xloc = petibmpy.linear_interpolation(wx, x, 1.3)
fig2, ax2 = create_plot(wx_xloc, z, y)
# Search for minimum in V5.
box = ((-0.6, -0.1), (0.3, 0.9))
points = add_extreme_values(ax2, wx_xloc, z, y, box, config='min', num=1)
z_V5, y_V5 = points[0][0], points[1][0]
print(f'V5: ({y_V5:.4f}, {z_V5:.4f})')
# Search for maximum in V6.
box = ((0.3, 0.8), (0.7, 1.3))
points = add_extreme_values(ax2, wx_xloc, z, y, box, config='max', num=1)
z_V6, y_V6 = points[0][-1], points[1][-1]
print(f'V6: ({y_V6:.4f}, {z_V6:.4f})')
# Search for maximum in V7.
box = ((-0.2, 0.2), (0.2, 0.9))
points = add_extreme_values(ax2, wx_xloc, z, y, box, config='max', num=1)
z_V7, y_V7 = points[0][-1], points[1][-1]
print(f'V7: ({y_V7:.4f}, {z_V7:.4f})')
# Search for minimum in V8.
box = ((-0.1, 0.4), (0.3, 1.3))
points = add_extreme_values(ax2, wx_xloc, z, y, box, config='min', num=1)
z_V8, y_V8 = points[0][0], points[1][0]
print(f'V8: ({y_V8:.4f}, {z_V8:.4f})')

print(f'd3 = {abs(z_V7 - z_V8):.4f}')
print(f'd4 = {abs(z_V5 - z_V6):.4f}')

pyplot.show()
