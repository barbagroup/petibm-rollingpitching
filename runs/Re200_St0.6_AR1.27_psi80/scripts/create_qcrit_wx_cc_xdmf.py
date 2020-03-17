"""Create a single XDMF file for the Q-criterion and the x-vorticity."""

import numpy
import pathlib
import yaml

import petibmpy


simudir = pathlib.Path(__file__).absolute().parents[1]
datadir = simudir / 'output'
outdir = datadir / 'postprocessing'
outdir.mkdir(parents=True, exist_ok=True)

# Get temporal parameters.
filepath = simudir / 'config.yaml'
with open(filepath, 'r') as infile:
    config = yaml.load(infile, Loader=yaml.FullLoader)
freq = config['bodies'][0]['kinematics']['f']
node = config['parameters']
dt, nstart, nt, nsave = (node[k] for k in ['dt', 'startStep', 'nt', 'nsave'])
timesteps = nstart + numpy.arange(0, nt + 1, nsave, dtype=numpy.int32)
times = dt * timesteps * freq

# Write the XDMF file to visualize with VisIt.
filepath = outdir / 'qcrit_wx_cc.xmf'
config = {'grid': outdir / 'qcrit' / 'grid.h5',
          'data': {'qcrit': outdir / 'qcrit',
                   'wx_cc': outdir / 'wx_cc'}}
petibmpy.write_xdmf_multi(filepath, config,
                          states=timesteps[1:], times=times[1:])
