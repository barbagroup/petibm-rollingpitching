"""Plot the isosurfaces of the Q-criterion at save time steps.

The isosurfaces are colored with the streamwise vorticity.
"""

import collections
import os

import sys
sys.path.insert(1, '/home/mesnardo/git/mesnardo/petibm-rollingpitching/src/python')

import visitplot


# Setup directories.
scriptdir = os.path.dirname(os.path.realpath(__file__))
simudir = os.path.dirname(scriptdir)
datadir = os.path.join(simudir, 'output')
figdir = os.path.join(simudir, 'figures')

# Path of the XDMF file.
xdmf_path = os.path.join(datadir, 'postprocessing', 'qcrit_wx_cc.xmf')

# Setup information about the views to plot.
View = collections.namedtuple('View', ['label', 'path', 'figsize'])
view1 = View(label='lateral',
             path=os.path.join(scriptdir, 'visit_lateral_view3d.yaml'),
             figsize=(800, 600))
view2 = View(label='top',
             path=os.path.join(scriptdir, 'visit_top_view3d.yaml'),
             figsize=(800, 400))
view3 = View(label='perspective',
             path=os.path.join(scriptdir, 'visit_perspective_view3d.yaml'),
             figsize=(850, 630))
views = [view1, view2, view3]

for view in views:
    prefix = 'qcrit_wx_{}_view_'.format(view.label)
    visitplot.visit_plot_qcrit_wx_3d(xdmf_path,
                                     qcrit_vals=(6.0, 1.0),
                                     wx_lims=(-5.0, 5.0),
                                     config_view=view.path,
                                     out_dir=figdir, prefix=prefix,
                                     figsize=view.figsize,
                                     state=17)
