"""Utility script to delete datasets from HDF5 files.

The script should be used to remove data generated at post-processing stage,
for example the vorticity components: `wx`, `wy`, and `wz`.
"""

import argparse
import pathlib
import yaml

import petibmpy


def parse_command_line():
    """Parse the command-line options."""
    formatter_class = argparse.ArgumentDefaultsHelpFormatter
    descr = 'Command-line parser to delete datasets from HDF5 files.'
    parser = argparse.ArgumentParser(description=descr,
                                     formatter_class=formatter_class)
    parser.add_argument('--simu-dir', dest='simudir',
                        type=str,
                        default='.',
                        help='Simulation directory')
    parser.add_argument('--names', dest='names',
                        nargs='+', type=str,
                        required=True,
                        help='Name of the datasets to delete')
    parser.add_argument('--timesteps', dest='timesteps',
                        nargs='+', type=int,
                        default=[],
                        help='Time-steps indices to consider')
    parser.add_argument('--range', dest='range',
                        nargs=3, type=int,
                        default=(None, None, None),
                        help='Time-step range to consider (min, max, step)')
    # Parse the command line and cast directory into a pathlib.Path object.
    args = parser.parse_args()
    args.simudir = pathlib.Path(args.simudir)
    return args


def config_get_timesteps(filepath):
    """Get list of time steps from YAML configuration file.

    Parameters
    ----------
    filepath : pathlib.Path or str
        Path of the YAML configuration file.

    Returns
    -------
    list
        List of time-step indices (as a list of integers).

    """
    with open(filepath, 'r') as infile:
        config = yaml.safe_load(infile)['parameters']
    config.setdefault('startStep', 0)
    nstart, nt, nsave = config['startStep'], config['nt'], config['nsave']
    return list(range(nstart, nt + 1, nsave))


# Parameters.
args = parse_command_line()
configpath = args.simudir / 'config.yaml'  # path of YAML configuration file
datadir = args.simudir / 'output'  # directory with HDF5 data

# Get the list of time-step indices to process.
if len(args.timesteps) == 0:
    if any(e is None for e in args.range):
        args.timesteps = config_get_timesteps(configpath)
    else:
        args.timesteps = list(range(args.range[0], args.range[1] + 1,
                                    args.range[2]))

# Delete gridlines from HDF5 grid file.
filepath = datadir / 'grid.h5'
print(f'INFO: Deleting datasets {args.names} from {filepath} ...')
petibmpy.delete_datasets_hdf5(filepath, args.names)

# Delete time-step data from HDF5 files.
for timestep in args.timesteps:
    filepath = datadir / f'{timestep:0>7}.h5'
    print(f'INFO: Deleting datasets {args.names} from {filepath} ...')
    petibmpy.delete_datasets_hdf5(filepath, args.names)

print('Done!')
