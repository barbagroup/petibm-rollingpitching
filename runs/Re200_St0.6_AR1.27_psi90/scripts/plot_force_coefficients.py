"""Plot the instantaneous force coefficients."""

from matplotlib import pyplot
import numpy
import pathlib

import rodney


args = rodney.parse_command_line()
display_kinematics = True  # Add kinematics to the figure
maindir = pathlib.Path(__file__).absolute().parents[1]

# Load force coefficients.
label = 'PetIBM'
simudir = maindir
config = rodney.WingKinematics(Re=200, nt_period=2000)
filepath = simudir / 'output' / 'forces-0.txt'
solution = rodney.load_force_coefficients(filepath, config)
rodney.print_stats(label, *rodney.get_stats(solution, limits=(3, 5)))

# Compute and print additional statistics (max of abs).
mask = numpy.where((solution.t >= 3) & (solution.t <= 5))[0]
ct, cl, cz = solution.ct[mask], solution.cl[mask], solution.cz[mask]
print('max(|C_T|)',  numpy.max(numpy.abs(ct)))
print('max(|C_L|)',  numpy.max(numpy.abs(cl)))
print('max(|C_Z|)',  numpy.max(numpy.abs(cz)))

# Plot the history of the force coefficients.
pyplot.rc('font', family='serif', size=12)
fig, (ax1, ax2, ax3) = pyplot.subplots(ncols=3, figsize=(12.0, 3.0))
xlim, ylim = (3.0, 5.0), (-6.0, 6.0)
# Plot the history of the thrust coefficient.
ax1.set_xlabel('$t / T$')
ax1.set_ylabel('$C_T$')
ax1.plot(solution.t, solution.ct, label=label, color='C3')
ax1.set_xlim(xlim)
ax1.set_ylim(ylim)
# Plot the history of the lift coefficient.
ax2.set_xlabel('$t / T$')
ax2.set_ylabel('$C_L$')
ax2.plot(solution.t, solution.cl, label=label, color='C3')
ax2.set_xlim(xlim)
ax2.set_ylim(ylim)
# Plot the history of the spanwise force coefficient.
ax3.set_xlabel('$t / T$')
ax3.set_ylabel('$C_Z$')
ax3.plot(solution.t, solution.cz, label=label, color='C3')
ax3.set_xlim(xlim)
ax3.set_ylim(ylim)

if display_kinematics:
    # Add the rolling and pitching kinematics to the figure.
    for ax in (ax1, ax2, ax3):
        axt = ax.twinx()
        axt.set_ylabel('Plate Rotation ($^o$)')
        axt.plot(solution.t,
                 numpy.degrees(config.rolling(solution.t * config.T)),
                 label='Rolling', color='C0', linestyle='--')
        axt.plot(solution.t,
                 numpy.degrees(config.pitching(solution.t * config.T)),
                 label='Pitching', color='C2', linestyle=':')
        axt.set_xlim(xlim)
        axt.set_ylim(-60.0, 60.0)

if args.extra_data:
    # Add the force coefficients from Li and Dong (2016).
    # The signals were digitized from Figure 9 of the article.
    scatter_kwargs = dict(s=10, facecolors='none', edgecolors='black')
    ax1.scatter(*rodney.li_dong_2016_load_ct(), label='Li & Dong (2016)',
                **scatter_kwargs)
    ax2.scatter(*rodney.li_dong_2016_load_cl(), label='Li & Dong (2016)',
                **scatter_kwargs)
    ax3.scatter(*rodney.li_dong_2016_load_cz(), label='Li & Dong (2016)',
                **scatter_kwargs)

ax1.legend(frameon=False, prop=dict(size=10), scatterpoints=3)
fig.tight_layout()

if args.save_figures:
    figdir = maindir / 'figures'
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'force_coefficients.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if args.show_figures:
    pyplot.show()
