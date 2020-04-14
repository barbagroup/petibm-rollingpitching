"""Create a single XDMF file for the Q-criterion and the x-vorticity."""

import pathlib

import petibmpy


simudir = pathlib.Path(__file__).absolute().parents[1]
datadir = simudir / 'output'
outdir = datadir / 'postprocessing'
outdir.mkdir(parents=True, exist_ok=True)

# List of time-step indices to include.
timesteps = [8500]

# Write the XDMF file to visualize with VisIt.
filepath = outdir / 'qcrit_wx_cc.xmf'
config = {'grid': outdir / 'qcrit' / 'grid.h5',
          'data': {'qcrit': outdir / 'qcrit',
                   'wx_cc': outdir / 'wx_cc'}}
petibmpy.write_xdmf_multi(filepath, config, states=timesteps)
