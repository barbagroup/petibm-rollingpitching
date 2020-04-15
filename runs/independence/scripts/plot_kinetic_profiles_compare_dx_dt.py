"""Plot profiles of the fluctuation of kinetic energy."""

from matplotlib import pyplot
import numpy
import pathlib
from scipy import interpolate

import rodney


def get_kinetic_energy_profiles(datadir, config, xlocs):
    """Get the profiles of kinetic energy at given time and x locations."""
    profiles = {'locs': None, 'vals': []}

    T = config.T  # period
    dt = config.dt  # time-step size
    nt_period = config.nt_period  # number of time steps per cycle
    # Set time values of the series.
    time_limits = (4 * T + dt, 5 * T)  # limits of the time series
    times = numpy.linspace(*time_limits, num=nt_period)[:-1]

    S = config.S  # spanwise length

    # Load the y locations to use for reference (for interpolation).
    # Staggered grids => y-locations are not the same for all velocity
    # components.
    filepath = datadir / 'probe1-u-kin.h5'
    y_ref, _ = rodney.get_vertical_profile_xy(filepath, 'u', times[0],
                                              xlocs[0], S / 2)
    profiles['locs'] = y_ref

    for iloc, xloc in enumerate(xlocs):
        kin = numpy.zeros_like(y_ref)
        for name in ('u', 'v', 'w'):
            filepath = datadir / f'probe{iloc + 1}-{name}-kin.h5'

            # Get the profile at each time values.
            series = []
            for time in times:
                y, vals = rodney.get_vertical_profile_xy(filepath, name,
                                                         time, xloc, S / 2)
                vals = interpolate.interpn((y,), vals, y_ref)
                series.append(vals)
            series = numpy.array(series)

            # Compute the mean velocity profile.
            avg = numpy.mean(series, axis=0)

            # Update the fluctuation of the kinetic energy
            # with the average of the fluctuation of the velocity component.
            kin += 0.5 * numpy.mean((series - avg)**2, axis=0)

        profiles['vals'].append(kin)

    return profiles


args = rodney.parse_command_line()
maindir = pathlib.Path(__file__).absolute().parents[1]
if args.save_figures:
    # Create directory for output figures.
    figdir = maindir / 'figures'
    figdir.mkdir(parents=True, exist_ok=True)
    figname_suffix = '_compare_dx_dt'

xlocs = [1.0, 2.0, 3.0, 4.0, 5.0]  # locations along the x-direction

all_profiles = []  # profiles for all simulations
plot_kwargs = []  # parameters for pyplot.plot function

# Simulation on nominal grid.
label = 'Nominal'
config = rodney.WingKinematics(Re=200.0, St=0.6, psi=90.0, nt_period=2000)
datadir = maindir / 'run3' / 'output'
all_profiles.append(get_kinetic_energy_profiles(datadir, config, xlocs))
plot_kwargs.append(dict(label=label, color='C3', linestyle='-'))

# Simulation on fine grid.
label = 'Finer in space'
config = rodney.WingKinematics(Re=200.0, St=0.6, psi=90.0, nt_period=2000)
datadir = maindir / 'run4' / 'output'
all_profiles.append(get_kinetic_energy_profiles(datadir, config, xlocs))
plot_kwargs.append(dict(label=label, color='black', linestyle='--'))

# Simulation on nominal grid with larger time-step size.
label = 'Coarser in time'
config = rodney.WingKinematics(Re=200.0, St=0.6, psi=90.0, nt_period=1000)
datadir = maindir / 'run6' / 'output'
all_profiles.append(get_kinetic_energy_profiles(datadir, config, xlocs))
plot_kwargs.append(dict(label=label, color='C0', linestyle='--'))

# Set default font style and size for Matplotlib figures.
pyplot.rc('font', family='serif', size=12)

# Plot the profiles of the fluctuation of kinetic energy
# in the x/y plane at z=S/2.
fig, ax = pyplot.subplots(figsize=(6.0, 5.0))
ax.set_xlabel('x/c')
ax.set_ylabel('y/c')
ax.axhline(0.0, color='black', linestyle='--')
for iloc, xloc in enumerate(xlocs):
    for profiles, kwargs in zip(all_profiles, plot_kwargs):
        if iloc > 0:
            kwargs = kwargs.copy()
            kwargs['label'] = None
        ax.plot(xloc + profiles['vals'][iloc], profiles['locs'], **kwargs)
if args.extra_data:
    # Add digitized data from Li & Dong (2016).
    ax.scatter(*rodney.li_dong_2016_load_kin_profiles(),
               label='Li & Dong (2016)',
               s=10, marker='o', edgecolor='black', color='none')
# ax.legend(frameon=False, prop={'size': 10}, loc='upper left')
ax.set_xlim(-2.0, 6.0)
ax.set_ylim(-3.0, 3.0)
fig.tight_layout()
if args.save_figures:
    # Save Matplotlib figure to PNG file.
    filepath = figdir / f'kin_profiles{figname_suffix}.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if args.show_figures:
    # Display Matplotlib figure.
    pyplot.show()
