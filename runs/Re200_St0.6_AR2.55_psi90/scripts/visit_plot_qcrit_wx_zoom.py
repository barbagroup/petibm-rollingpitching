"""Plot the isosurfaces of the Q-criterion at save time steps.

The isosurfaces are colored with the streamwise vorticity.
"""

import collections
import os

import visitplot


# Setup directories.
scriptdir = os.path.dirname(os.path.realpath(__file__))
simudir = os.path.dirname(scriptdir)
datadir = os.path.join(simudir, 'output')
figdir = os.path.join(simudir, 'figures')

# Path of the XDMF file.
xdmf_path = os.path.join(datadir, 'postprocessing', 'qcrit_wx_cc.xmf')

# Setup information about the view to plot.
View = collections.namedtuple('View', ['label', 'path', 'figsize'])
view = View(label='perspective_zoom',
            path=os.path.join(scriptdir, 'visit_perspective_zoom_view3d.yaml'),
            figsize=(600, 600))

prefix = 'qcrit_wx_{}_view_'.format(view.label)
visitplot.visit_plot_qcrit_wx_3d(xdmf_path,
                                 qcrit_vals=(6.0, 1.0),
                                 wx_lims=(-5.0, 5.0),
                                 config_view=view.path,
                                 out_dir=figdir, prefix=prefix,
                                 figsize=view.figsize)
