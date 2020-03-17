"""Plot the history of the force coefficients."""

from matplotlib import pyplot
import numpy
import pathlib

import rodney


args = rodney.parse_command_line()
display_kinematics = False  # Add kinematics to the figure

# Load force coefficients.
label = 'Re=200, St=0.8, AR=1.27, psi=90'
simudir = pathlib.Path(__file__).absolute().parents[1]
config = rodney.WingKinematics(Re=200, St=1.0, nt_period=2000)
filepath = simudir / 'output' / 'forces-0.txt'
solution = rodney.load_force_coefficients(filepath, config)
means, rms = rodney.get_stats(solution, limits=(3, 5))
rodney.print_stats(label, means, rms)

# Plot the history of the force coefficients.
pyplot.rc('font', family='serif', size=12)
fig, (ax1, ax2, ax3) = pyplot.subplots(ncols=3, figsize=(12.0, 3.0))
xlim, ylim = (3.0, 5.0), (-6.0, 6.0)
# Plot the history of the thrust coefficient.
ax1.set_xlabel('$t / T$')
ax1.set_ylabel('$C_T$')
ax1.plot(solution.t, solution.ct, label=label)
ax1.axhline(means.ct, color='C3', linestyle='-')
ax1.set_xlim(xlim)
ax1.set_ylim(ylim)
# Plot the history of the lift coefficient.
ax2.set_xlabel('$t / T$')
ax2.set_ylabel('$C_L$')
ax2.plot(solution.t, solution.cl, label=label)
ax2.axhline(means.cl, color='C3', linestyle='-')
ax2.set_xlim(xlim)
ax2.set_ylim(ylim)
# Plot the history of the spanwise force coefficient.
ax3.set_xlabel('$t / T$')
ax3.set_ylabel('$C_Z$')
ax3.plot(solution.t, solution.cz, label=label)
ax3.axhline(means.cz, color='C3', linestyle='-')
ax3.set_xlim(xlim)
ax3.set_ylim(ylim)

if display_kinematics:
    # Add the rolling and pitching kinematics to the figure.
    for ax in (ax1, ax2, ax3):
        axt = ax.twinx()
        axt.set_ylabel('Plate Rotation ($^o$)')
        axt.plot(solution.t,
                 numpy.degrees(config.rolling(solution.t * config.T)),
                 label='Rolling', color='black', linestyle='--')
        axt.plot(solution.t,
                 numpy.degrees(config.pitching(solution.t * config.T)),
                 label='Pitching', color='black', linestyle=':')
        axt.set_xlim(xlim)
        axt.set_ylim(-60.0, 60.0)

ax1.legend(frameon=False, prop=dict(size=10))
fig.tight_layout()

if args.save_figures:
    figdir = simudir / 'figures'
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'force_coefficients.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if args.show_figures:
    pyplot.show()
