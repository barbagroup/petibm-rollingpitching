"""Compute the Q-criterion."""

import pathlib

import petibmpy


name = 'qcrit'
simudir = pathlib.Path(__file__).absolute().parents[1]
datadir = simudir / 'output'
gridpath = datadir / 'grid.h5'
outdir = datadir / 'postprocessing' / name
outdir.mkdir(parents=True, exist_ok=True)

# Read the cell-centered grid.
x, y, z = petibmpy.read_grid_hdf5(gridpath, 'p')
# Read the grid of the velocity components.
grid_u = petibmpy.read_grid_hdf5(gridpath, 'u')
grid_v = petibmpy.read_grid_hdf5(gridpath, 'v')
grid_w = petibmpy.read_grid_hdf5(gridpath, 'w')

# Save the grid on which is defined the Q-criterion.
gridpath = outdir / 'grid.h5'
petibmpy.write_grid_hdf5(gridpath, name, x, y, z)

# List of time-step indices to process.
timesteps = [8500]

interp_args = dict(bounds_error=False, method='linear', fill_value=None)
for timestep in timesteps:
    print('[time step {}] Computing the Q-criterion ...'.format(timestep))
    filepath = datadir / '{:0>7}.h5'.format(timestep)
    # Load and interpolate the velocity field on the cell-centered grid.
    u = petibmpy.read_field_hdf5(filepath, 'u')
    u = petibmpy.interpolate3d(u, grid_u, (x, y, z), **interp_args)
    v = petibmpy.read_field_hdf5(filepath, 'v')
    v = petibmpy.interpolate3d(v, grid_v, (x, y, z), **interp_args)
    w = petibmpy.read_field_hdf5(filepath, 'w')
    w = petibmpy.interpolate3d(w, grid_w, (x, y, z), **interp_args)
    # Compute the Q-criterion.
    qcrit = petibmpy.qcriterion((u, v, w), (x, y, z))
    # Save the Q-criterion into file.
    filepath = outdir / '{:0>7}.h5'.format(timestep)
    petibmpy.write_field_hdf5(filepath, name, qcrit)

# Write the XDMF file to visualize with VisIt.
filepath = outdir / (name + '.xmf')
petibmpy.write_xdmf(filepath, outdir, gridpath, name, states=timesteps)
