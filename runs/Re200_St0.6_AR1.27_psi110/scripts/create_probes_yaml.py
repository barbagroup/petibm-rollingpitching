"""Write the YAML configuration file for the probes."""

import numpy
import pathlib
import yaml

import petibmpy

import rodney


# Set the simulation directory.
simudir = pathlib.Path(__file__).absolute().parents[1]
datadir = simudir / 'output'

# Set the kinematics of the wing.
config = rodney.WingKinematics(psi=110.0, Re=200, St=0.6, nt_period=2000)

c, S, A_phi = config.c, config.S, config.A_phi
n_periods, nt_period = config.n_periods, config.nt_period
dt = config.dt

probes = []  # will store info about the probes

# Set probe information for the x- and y- components of the velocity.
fields = ['u', 'v']
for field in fields:
    filepath = datadir / 'grid.h5'
    grid = petibmpy.read_grid_hdf5(filepath, field)
    xlocs = [1.0, 2.0, 3.0, 4.0, 5.0]
    for i, xloc in enumerate(xlocs):
        name = f'probe{i + 1}-{field}'
        box = ((xloc, xloc), (-3.0, 3.0), (S / 2, S / 2))
        probe = petibmpy.ProbeVolume(name, field,
                                     box=box, adjust_box=True, grid=grid,
                                     n_sum=nt_period,
                                     path=f'{name}.h5')
        probes.append(probe)

# Set probe information for the z-component of the velocity.
fields = ['w']
for field in fields:
    filepath = datadir / 'grid.h5'
    grid = petibmpy.read_grid_hdf5(filepath, field)
    xlocs = [1.0, 2.0, 3.0, 4.0, 5.0]
    for i, xloc in enumerate(xlocs):
        name = f'probe{i + 1}-{field}'
        box = ((xloc, xloc), (0.0, 0.0), (-3.0, 3.0))
        probe = petibmpy.ProbeVolume(name, field,
                                     box=box, adjust_box=True, grid=grid,
                                     n_sum=nt_period,
                                     path=f'{name}.h5')
        probes.append(probe)

# Set probe information to get fluctuation of the kinetic energy.
fields = ['u', 'v', 'w']
for field in fields:
    filepath = datadir / 'grid.h5'
    grid = petibmpy.read_grid_hdf5(filepath, field)
    xlocs = [1.0, 2.0, 3.0, 4.0, 5.0]
    for i, xloc in enumerate(xlocs):
        name = f'probe{i + 1}-{field}-kin'
        box = ((xloc, xloc), (-3.0, 3.0), (S / 2, S / 2))
        t_start = (n_periods - 1) * nt_period * dt
        t_end = n_periods * nt_period * dt
        probe = petibmpy.ProbeVolume(name, field,
                                     box=box, adjust_box=True, grid=grid,
                                     t_start=float(t_start),
                                     t_end=float(t_end),
                                     path=f'{name}.h5')
        probes.append(probe)

# Set probe information for the velocity and pressure in the fine region.
fields = ['u', 'v', 'w', 'p']
buf = 0.05 * c
for field in fields:
    filepath = datadir / 'grid.h5'
    grid = petibmpy.read_grid_hdf5(filepath, field)
    xlim = (-c / 2 - buf, c / 2 + buf)
    ylim = (-S * numpy.cos(A_phi) - buf, S * numpy.cos(A_phi) + buf)
    zlim = (0.0 - buf, S + buf)
    box = (xlim, ylim, zlim)
    name = f'probe_vicinity-{field}'
    t_start = (n_periods - 1) * nt_period * dt
    t_end = n_periods * nt_period * dt
    probe = petibmpy.ProbeVolume(name, field,
                                 box=box, adjust_box=True, grid=grid,
                                 t_start=float(t_start), t_end=float(t_end),
                                 n_monitor=round(nt_period / 200),
                                 path=f'{name}.h5')
    probes.append(probe)

# Load the probe information to a YAML file.
filepath = simudir / 'probes.yaml'
petibmpy.probes_yaml_dump(probes, filepath)
