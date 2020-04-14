"""Plot the instantaneous force coefficients."""

from matplotlib import pyplot
import pathlib

import rodney


args = rodney.parse_command_line()
maindir = pathlib.Path(__file__).absolute().parents[1]

# Load force coefficients for simulation with AR=1.27.
label = 'AR = 1.27'
simudir = maindir / 'Re200_St0.6_AR1.27_psi90'
config = rodney.WingKinematics(Re=200, AR=1.27, nt_period=2000)
filepath = simudir / 'output' / 'forces-0.txt'
solution = rodney.load_force_coefficients(filepath, config)
rodney.print_stats(label, *rodney.get_stats(solution, limits=(3, 5)))
plot_kwargs = dict(color='C3', linestyle='-')

# Load force coefficients for simulation with AR=1.91.
label2 = 'AR = 1.91'
simudir2 = maindir / 'Re200_St0.6_AR1.91_psi90'
config2 = rodney.WingKinematics(Re=200, AR=1.91, nt_period=2000)
filepath = simudir2 / 'output' / 'forces-0.txt'
solution2 = rodney.load_force_coefficients(filepath, config2)
rodney.print_stats(label2, *rodney.get_stats(solution2, limits=(3, 5)))
plot_kwargs2 = dict(color='black', linestyle='--')

# Plot the history of the force coefficients.
pyplot.rc('font', family='serif', size=12)
fig, (ax1, ax2, ax3) = pyplot.subplots(ncols=3, figsize=(12.0, 3.0))
xlim, ylim = (3.0, 5.0), (-6.0, 6.0)
# Plot the history of the thrust coefficient.
ax1.set_xlabel('$t / T$')
ax1.set_ylabel('$C_T$')
ax1.plot(solution.t, solution.ct, label=label, **plot_kwargs)
ax1.plot(solution2.t, solution2.ct, label=label2, **plot_kwargs2)
ax1.set_xlim(xlim)
ax1.set_ylim(ylim)
# Plot the history of the lift coefficient.
ax2.set_xlabel('$t / T$')
ax2.set_ylabel('$C_L$')
ax2.plot(solution.t, solution.cl, label=label, **plot_kwargs)
ax2.plot(solution2.t, solution2.cl, label=label2, **plot_kwargs2)
ax2.set_xlim(xlim)
ax2.set_ylim(ylim)
# Plot the history of the spanwise force coefficient.
ax3.set_xlabel('$t / T$')
ax3.set_ylabel('$C_Z$')
ax3.plot(solution.t, solution.cz, label=label, **plot_kwargs)
ax3.plot(solution2.t, solution2.cz, label=label2, **plot_kwargs2)
ax3.set_xlim(xlim)
ax3.set_ylim(ylim)

ax1.legend(frameon=False)
fig.tight_layout()

if args.save_figures:
    figdir = maindir / 'figures'
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'force_coefficients_compare_AR.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if args.show_figures:
    pyplot.show()
