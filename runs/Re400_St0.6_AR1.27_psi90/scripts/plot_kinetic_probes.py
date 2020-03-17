"""Plot profiles of the fluctuation of kinetic energy."""

from matplotlib import pyplot
import numpy
import pathlib
from scipy import interpolate

import rodney

from kinematics import S, T, dt, nt_period


def get_kinetic_energy_profiles(datadir, times, xlocs):
    """Get the profiles of kinetic energy at given time and x locations."""
    profiles = {'locs': None, 'vals': []}

    # Load the y locations to use for reference (for interpolation).
    # Staggered grids => y-locations are not the same for all velocity
    # components.
    filepath = datadir / 'probe1-u-kin.h5'
    y_ref, _ = rodney.get_vertical_profile_xy(filepath, 'u', times[0],
                                              xlocs[0], S / 2)
    profiles['locs'] = y_ref

    # Loop over the different x locations in the wake.
    for iloc, xloc in enumerate(xlocs):
        # Initialize array for the fluctuations of the kinetic energy.
        kin = numpy.zeros_like(y_ref)
        # Loop over the velocity components.
        for name in ('u', 'v', 'w'):
            # Path with data of the profiles.
            filepath = datadir / f'probe{iloc + 1}-{name}-kin.h5'

            # Get the profile at each time values.
            series = numpy.empty((times.size, y_ref.size))
            for n, time in enumerate(times):
                # Load vertical profile of the velocity component
                # in the x/y plane at midspan (z = S / 2).
                y, vals = rodney.get_vertical_profile_xy(filepath, name,
                                                         time, xloc, S / 2)
                # Interpolate profile at y locations used for reference.
                # Add to series.
                series[n] = interpolate.interpn((y,), vals, y_ref)

            # Compute the mean velocity component (average over the time).
            avg = numpy.mean(series, axis=0)

            # Update the fluctuations of the kinetic energy average (over time)
            # of the fluctuations of the velocity component.
            kin += 0.5 * numpy.mean((series - avg)**2, axis=0)

        # Add profile of kinetic energy obtained at wake location `xloc`.
        profiles['vals'].append(kin)

    return profiles


args = rodney.parse_command_line()
maindir = pathlib.Path(__file__).absolute().parents[1]
if args.save_figures:
    # Create directory for output figures.
    figdir = maindir / 'figures'
    fig_suffix = ''
    figdir.mkdir(parents=True, exist_ok=True)

# Set time values of the series.
time_limits = (4 * T + dt, 5 * T)  # limits of the time series
times = numpy.linspace(*time_limits, num=nt_period)[:-1]

xlocs = [1.0, 2.0, 3.0, 4.0, 5.0]  # locations along the x-direction

all_profiles = []  # profiles for all simulations
plot_kwargs = []  # parameters for pyplot.plot function

# Load velocity profiles and compute fluctuations of kinetic energy.
label = r'$\Delta x / c = 0.01$'
simudir = maindir
all_profiles.append(get_kinetic_energy_profiles(simudir / 'output',
                                                times, xlocs))
plot_kwargs.append(dict(label=label, color='C3'))

# Set default font style and size for Matplotlib figures.
pyplot.rc('font', family='serif', size=14)

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
               s=20, marker='o', edgecolor='black', color='none')
ax.legend(frameon=False, prop={'size': 10})
ax.set_xlim(-2.0, 6.0)
ax.set_ylim(-3.0, 3.0)
fig.tight_layout()
if args.save_figures:
    # Save Matplotlib figure to PNG file.
    filepath = figdir / f'kin_profiles{fig_suffix}.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if args.show_figures:
    # Display Matplotlib figure.
    pyplot.show()
