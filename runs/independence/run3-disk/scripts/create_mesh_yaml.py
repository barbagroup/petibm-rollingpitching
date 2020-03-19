"""Create a YAML file with info about the structured Cartesian mesh."""

import collections
from matplotlib import pyplot
import numpy
import pathlib

import petibmpy


def get_gridline_config(p1, p2, p3, p4, p5, p6, d1, d2, r1, r2, r3, r4):
    """Create configuration of sub-domains along a direction."""
    cfg = []
    cfg.append(dict(start=p1, end=p2, width=d1, stretchRatio=r1,
                    reverse=True))
    cfg.append(dict(start=p2, end=p3, width=d2, stretchRatio=r2, max_width=d1,
                    reverse=True))
    cfg.append(dict(start=p3, end=p4, width=d2))
    cfg.append(dict(start=p4, end=p5, width=d2, stretchRatio=r3, max_width=d1))
    cfg.append(dict(start=p5, end=p6, width=d1, stretchRatio=r4))
    return cfg


Box = collections.namedtuple('Box', ['xstart', 'xend',
                                     'ystart', 'yend',
                                     'zstart', 'zend'])

box1 = Box(-15.0, 15.0, -12.5, 12.5, -12.5, 12.5)
box2, width2 = Box(-2.0, 6.0, -3.0, 3.0, -1.0, 2.0), 0.05
box3, width3 = Box(-1.1, 2.2, -1.05, 1.05, -0.55, 1.55), 0.01
show_figure = True

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
