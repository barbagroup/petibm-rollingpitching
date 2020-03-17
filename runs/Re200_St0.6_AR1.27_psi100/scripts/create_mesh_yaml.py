"""Create a YAML file with info about the structured Cartesian mesh."""

import collections
import math
from matplotlib import pyplot
import numpy
import pathlib

import petibmpy

import rodney


def get_gridline_config(p1, p2, p3, p4, p5, p6, d1, d2, r1, r2, r3, r4):
    """Create configuration of sub-domains along a direction."""
    cfg = []
    cfg.append(dict(start=p1, end=p2, width=d1, stretchRatio=r1,
                    max_width=20 * d1, reverse=True))
    cfg.append(dict(start=p2, end=p3, width=d2, stretchRatio=r2, max_width=d1,
                    reverse=True))
    cfg.append(dict(start=p3, end=p4, width=d2))
    cfg.append(dict(start=p4, end=p5, width=d2, stretchRatio=r3, max_width=d1))
    cfg.append(dict(start=p5, end=p6, width=d1, stretchRatio=r4,
                    max_width=20 * d1))
    return cfg


def resize_for_uniform(L, xc, dx, buf=0.0):
    """Adjust the limits of the interval to allow uniform discretization."""
    xs, xe = xc - L / 2 - buf, xc + L / 2 + buf
    L = xe - xs
    n = math.ceil(L / dx)
    L = n * dx
    xs, xe = xc - L / 2, xc + L / 2
    assert abs((xe - xs) / n - dx) < 1e-12
    return xs, xe


Box = collections.namedtuple('Box', ['xstart', 'xend',
                                     'ystart', 'yend',
                                     'zstart', 'zend'])

config = rodney.WingKinematics(psi=100.0, Re=200, St=0.6, nt_period=2000)
c, S, A_phi = config.c, config.S, config.A_phi

box1 = Box(-15.0, 15.0, -12.5, 12.5, -12.5, 12.5)
box2, width2 = Box(-2.0, 6.0, -3.0, 3.0, -1.0, 2.0), 0.05 * c

dx = 0.01 * c
buf = 0.05 * c
xs, xe = resize_for_uniform(c, 0.0, dx, buf=buf)
ys, ye = resize_for_uniform(2 * S * numpy.cos(A_phi), 0.0, dx, buf=buf)
zs, ze = resize_for_uniform(S, S / 2, dx, buf=buf)
box3, width3 = Box(xs, xe, ys, ye, zs, ze), dx

show_figure = False

config_x = get_gridline_config(box1.xstart, box2.xstart, box3.xstart,
                               box3.xend, box2.xend, box1.xend,
                               width2, width3, 1.2, 1.1, 1.03, 1.2)
config_y = get_gridline_config(box1.ystart, box2.ystart, box3.ystart,
                               box3.yend, box2.yend, box1.yend,
                               width2, width3, 1.2, 1.1, 1.1, 1.2)
config_z = get_gridline_config(box1.zstart, box2.zstart, box3.zstart,
                               box3.zend, box2.zend, box1.zend,
                               width2, width3, 1.2, 1.1, 1.1, 1.2)

config = [dict(direction='x', start=box1.xstart, subDomains=config_x),
          dict(direction='y', start=box1.ystart, subDomains=config_y),
          dict(direction='z', start=box1.zstart, subDomains=config_z)]

grid = petibmpy.CartesianGrid(config)
print(grid)
simudir = pathlib.Path(__file__).absolute().parents[1]
filepath = simudir / 'mesh.yaml'
grid.write_yaml(filepath, ndigits=10)
grid.print_info()

if show_figure:
    fig, ax = grid.plot_gridlines()
    fig.tight_layout()
    pyplot.show()
