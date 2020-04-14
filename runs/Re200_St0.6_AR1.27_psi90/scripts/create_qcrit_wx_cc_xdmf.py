"""Create a single XDMF file for the Q-criterion and the x-vorticity."""

import pathlib

import petibmpy


# Set directories.
simudir = pathlib.Path(__file__).absolute().parents[1]
datadir = simudir / 'output'
outdir = datadir / 'postprocessing'
outdir.mkdir(parents=True, exist_ok=True)

# Get list of time-step indices to include in XDMF file.
timesteps = [7750, 7875, 8000, 8250, 8375, 8500, 8625, 8750, 8875]

# Write the XDMF file to visualize with VisIt.
filepath = outdir / 'qcrit_wx_cc.xmf'
config = {'grid': outdir / 'qcrit' / 'grid.h5',
          'data': {'qcrit': outdir / 'qcrit',
                   'wx_cc': outdir / 'wx_cc'}}
petibmpy.write_xdmf_multi(filepath, config, states=timesteps)
