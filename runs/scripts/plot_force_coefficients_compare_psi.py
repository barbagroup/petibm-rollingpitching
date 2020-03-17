"""Plot the instantaneous force coefficients."""

from matplotlib import pyplot
import pathlib

import rodney


args = rodney.parse_command_line()
maindir = pathlib.Path(__file__).absolute().parents[1]

# Load force coefficients for simulation with psi=90.
label = r'$\psi = 90^o$'
simudir = maindir / 'Re200_St0.6_AR1.27_psi90'
config = rodney.WingKinematics(psi=90.0)
filepath = simudir / 'output' / 'forces-0.txt'
solution = rodney.load_force_coefficients(filepath, config)
rodney.print_stats(label, *rodney.get_stats(solution, limits=(3, 5)))

# Load force coefficients for simulation with psi=100.
label2 = r'$\psi = 100^o$'
simudir2 = maindir / 'Re200_St0.6_AR1.27_psi100'
config2 = rodney.WingKinematics(psi=100.0)
filepath = simudir2 / 'output' / 'forces-0.txt'
solution2 = rodney.load_force_coefficients(filepath, config2)
rodney.print_stats(label2, *rodney.get_stats(solution2, limits=(3, 5)))

# Load force coefficients for simulation with psi=110.
label3 = r'$\psi = 110^o$'
simudir3 = maindir / 'Re200_St0.6_AR1.27_psi110'
config3 = rodney.WingKinematics(psi=110.0)
filepath = simudir3 / 'output' / 'forces-0.txt'
solution3 = rodney.load_force_coefficients(filepath, config3)
rodney.print_stats(label3, *rodney.get_stats(solution3, limits=(3, 5)))

# Load force coefficients for simulation with psi=120.
label4 = r'$\psi = 120^o$'
simudir4 = maindir / 'Re200_St0.6_AR1.27_psi120'
config4 = rodney.WingKinematics(psi=120.0)
filepath = simudir4 / 'output' / 'forces-0.txt'
solution4 = rodney.load_force_coefficients(filepath, config4)
rodney.print_stats(label4, *rodney.get_stats(solution4, limits=(3, 5)))

# Plot the history of the force coefficients.
pyplot.rc('font', family='serif', size=12)
fig, (ax1, ax2, ax3) = pyplot.subplots(ncols=3, figsize=(12.0, 3.0))
xlim = (3.0, 5.0)
# Plot the history of the thrust coefficient.
ax1.set_xlabel('$t / T$')
ax1.set_ylabel('$C_T$')
ax1.plot(solution.t, solution.ct, label=label)
ax1.plot(solution2.t, solution2.ct, label=label2)
ax1.plot(solution3.t, solution3.ct, label=label3)
ax1.plot(solution4.t, solution4.ct, label=label4)
ax1.set_xlim(xlim)
ax1.set_ylim(-8.0, 8.0)
# Plot the history of the lift coefficient.
ax2.set_xlabel('$t / T$')
ax2.set_ylabel('$C_L$')
ax2.plot(solution.t, solution.cl, label=label)
ax2.plot(solution2.t, solution2.cl, label=label2)
ax2.plot(solution3.t, solution3.cl, label=label3)
ax2.plot(solution4.t, solution4.cl, label=label4)
ax2.set_xlim(xlim)
ax2.set_ylim(-15.0, 15.0)
# Plot the history of the spanwise force coefficient.
ax3.set_xlabel('$t / T$')
ax3.set_ylabel('$C_Z$')
ax3.plot(solution.t, solution.cz, label=label)
ax3.plot(solution2.t, solution2.cz, label=label2)
ax3.plot(solution3.t, solution3.cz, label=label3)
ax3.plot(solution4.t, solution4.cz, label=label4)
ax3.set_xlim(xlim)
ax3.set_ylim(-8.0, 8.0)

ax1.legend(ncol=2, frameon=False)
fig.tight_layout()

if args.save_figures:
    figdir = maindir / 'figures'
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'force_coefficients_compare_psi.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if args.show_figures:
    pyplot.show()
