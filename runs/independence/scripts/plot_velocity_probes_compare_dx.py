"""Plot profiles of the velocity at different locations in the x direction."""

from matplotlib import pyplot
import pathlib

import rodney


def get_velocity_profiles(datadir,config, time, xlocs):
    """Get the velocity profiles at given time and x locations."""
    profiles = {'u': {'locs': None, 'vals': []},
                'v': {'locs': None, 'vals': []},
                'w': {'locs': None, 'vals': []}}
    get_profile = {'u': rodney.get_vertical_profile_xy,
                   'v': rodney.get_vertical_profile_xy,
                   'w': rodney.get_spanwise_profile_xz}
    S = config.S  # spanwise length
    yzloc = {'u': S / 2, 'v': S / 2, 'w': 0.0}
    for name in profiles.keys():
        for iloc, xloc in enumerate(xlocs):
            filepath = datadir / f'probe{iloc + 1}-{name}.h5'
            locs, vals = get_profile[name](filepath, name, time,
                                           xloc, yzloc[name])
            profiles[name]['vals'].append(vals)
        profiles[name]['locs'] = locs
    return profiles


args = rodney.parse_command_line()
maindir = pathlib.Path(__file__).absolute().parents[1]

if args.save_figures:
    # Create directory for output figures.
    figdir = maindir / 'figures'
    figdir.mkdir(parents=True, exist_ok=True)
    figname_suffix = '_compare_dx'

time = 6.528332  # time value to get data over the last cycle
xlocs = [1.0, 2.0, 3.0, 4.0, 5.0]  # locations along the x-direction

all_profiles = []  # profiles for all simulations
plot_kwargs = []  # parameters for pyplot.plot function

# Compute velocity profiles obtained with coarse grid.
label = r'$\Delta x / c = 0.03$'
datadir = maindir / 'run1' / 'output'
config = rodney.WingKinematics(nt_period=1000)
all_profiles.append(get_velocity_profiles(datadir, config, time, xlocs))
plot_kwargs.append(dict(label=label, color='C0', linestyle='-'))

# Compute velocity profiles obtained with intermediate grid.
label = r'$\Delta x / c = 0.015$'
datadir = maindir / 'run2' / 'output'
config = rodney.WingKinematics(nt_period=1000)
all_profiles.append(get_velocity_profiles(datadir, config, time, xlocs))
plot_kwargs.append(dict(label=label, color='C3', linestyle='-'))

# Compute velocity profiles obtained with finer grid.
label = r'$\Delta x / c = 0.01$'
datadir = maindir / 'run3' / 'output'
config = rodney.WingKinematics(nt_period=1000)
all_profiles.append(get_velocity_profiles(datadir, config, time, xlocs))
plot_kwargs.append(dict(label=label, color='black', linestyle='--'))


# Set default font style and size for Matplotlib figures.
pyplot.rc('font', family='serif', size=12)

# Plot the x-velocity profiles in the x/y plane at z=S/2.
fig, ax = pyplot.subplots(figsize=(6.0, 5.0))
ax.set_xlabel('x/c')
ax.set_ylabel('y/c')
ax.axhline(0.0, color='grey', linestyle='--')
for iloc, xloc in enumerate(xlocs):
    for profiles, kwargs in zip(all_profiles, plot_kwargs):
        if iloc > 0:
            kwargs = kwargs.copy()
            kwargs['label'] = None
        ax.plot(xloc + profiles['u']['vals'][iloc] - config.U_inf,
                profiles['u']['locs'], **kwargs)
if args.extra_data:
    # Add digitized data from Li & Dong (2016).
    ax.scatter(*rodney.li_dong_2016_load_ux_profiles(),
               label='Li & Dong (2016)',
               s=10, marker='o', edgecolor='black', color='none')
ax.legend(frameon=False, prop={'size': 10})
ax.set_xlim(-2.0, 6.0)
ax.set_ylim(-3.0, 3.0)
fig.tight_layout()
if args.save_figures:
    # Save Matplotlib figure to PNG file.
    filepath = figdir / f'ux_profiles{figname_suffix}.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

# Plot the y-velocity profiles in the x/y plane at z=S/2.
fig, ax = pyplot.subplots(figsize=(6.0, 5.0))
ax.set_xlabel('x/c')
ax.set_ylabel('y/c')
ax.axhline(0.0, color='grey', linestyle='--')
for iloc, xloc in enumerate(xlocs):
    for profiles, kwargs in zip(all_profiles, plot_kwargs):
        if iloc > 0:
            kwargs = kwargs.copy()
            kwargs['label'] = None
        ax.plot(xloc + profiles['v']['vals'][iloc],
                profiles['v']['locs'], **kwargs)
if args.extra_data:
    # Add digitized data from Li & Dong (2016).
    ax.scatter(*rodney.li_dong_2016_load_uy_profiles(),
               label='Li & Dong (2016)',
               s=10, marker='o', edgecolor='black', color='none')
ax.legend(frameon=False, prop={'size': 10})
ax.set_xlim(-2.0, 6.0)
ax.set_ylim(-3.0, 3.0)
fig.tight_layout()
if args.save_figures:
    # Save Matplotlib figure to PNG file.
    filepath = figdir / f'uy_profiles{figname_suffix}.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

# Plot the z-velocity profiles in the x/z plane at y=0.
fig, ax = pyplot.subplots(figsize=(6.0, 5.0))
ax.set_xlabel('x/c')
ax.set_ylabel('z/c')
ax.axhline(0.0, color='grey', linestyle='--')
for iloc, xloc in enumerate(xlocs):
    for profiles, kwargs in zip(all_profiles, plot_kwargs):
        if iloc > 0:
            kwargs = kwargs.copy()
            kwargs['label'] = None
        ax.plot(xloc + profiles['w']['vals'][iloc],
                profiles['w']['locs'] - config.S / 2, **kwargs)
if args.extra_data:
    # Add digitized data from Li & Dong (2016).
    ax.scatter(*rodney.li_dong_2016_load_uz_profiles(),
               label='Li & Dong (2016)',
               s=10, marker='o', edgecolor='black', color='none')
ax.legend(frameon=False, prop={'size': 10})
ax.set_xlim(-2.0, 6.0)
ax.set_ylim(-2.0, 2.0)
fig.tight_layout()
if args.save_figures:
    # Save Matplotlib figure to PNG file.
    filepath = figdir / f'uz_profiles{figname_suffix}.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if args.show_figures:
    # Display Matplotlib figure.
    pyplot.show()
