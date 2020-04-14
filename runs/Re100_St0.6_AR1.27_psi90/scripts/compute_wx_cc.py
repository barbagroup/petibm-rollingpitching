"""Compute the cell-centered x-component of the vorticity."""

import pathlib
import yaml

import petibmpy


name = 'wx_cc'
simudir = pathlib.Path(__file__).absolute().parents[1]
datadir = simudir / 'output'
gridpath = datadir / 'grid.h5'
outdir = datadir / 'postprocessing' / name
outdir.mkdir(parents=True, exist_ok=True)

# Read the cell-centered grid.
x, y, z = petibmpy.read_grid_hdf5(gridpath, 'p')
# Read the grid of the x-component of the vorticity.
grid_wx = petibmpy.read_grid_hdf5(gridpath, 'wx')

# Save the grid on which is defined the Q-criterion.
gridpath = outdir / 'grid.h5'
petibmpy.write_grid_hdf5(gridpath, name, x, y, z)

# List of time-step indices to process.
timesteps = [8500]

interp_args = dict(bounds_error=False, method='linear', fill_value=None)
for timestep in timesteps:
    print('[time step {}] Computing the cell-centered x-vorticity ...'
          .format(timestep))
    filepath = datadir / '{:0>7}.h5'.format(timestep)
    # Load and interpolate the x-vorticity field on the cell-centered grid.
    wx = petibmpy.read_field_hdf5(filepath, 'wx')
    wx = petibmpy.interpolate3d(wx, grid_wx, (x, y, z), **interp_args)
    # Save the cell-centered x-vorticity field into file.
    filepath = outdir / '{:0>7}.h5'.format(timestep)
    petibmpy.write_field_hdf5(filepath, name, wx)

# Write the XDMF file to visualize with VisIt.
filepath = outdir / (name + '.xmf')
petibmpy.write_xdmf(filepath, outdir, gridpath, name, states=timesteps)
