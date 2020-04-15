"""Plot the propulsive efficiency and cycle-averaged trust coefficient.

Plot agains the Strouhal number.
"""

from matplotlib import pyplot
import pathlib

import rodney


args = rodney.parse_command_line()
maindir = pathlib.Path(__file__).absolute().parents[1]
figdir = maindir / 'figures'

# Hard-coded for now.
psi_values = [60, 70, 80, 90, 100, 110, 120]
ct_values = [0.2114, 0.4591, 0.6835, 0.9138, 1.1306, 1.3276, 1.4904]
eta_values = [0.0296, 0.0758, 0.1236, 0.1635, 0.1814, 0.1772, 0.1603]

pyplot.rc('font', family='serif', size=12)
fig, ax = pyplot.subplots(figsize=(6.0, 4.0))
# Plot cycle-averaged thrust coefficient versus phase difference.
ax.set_xlabel(r'$\psi$')
label = r'$\overline{C_T}$'
ax.set_ylabel(label)
ax.plot(psi_values, ct_values, label=label, color='C3', marker='o')
ax.set_ylim(0.0, 3.0)
# Plot cycle-averaged propulsive efficiency versus phase difference.
axb = ax.twinx()
label = r'$\eta$'
axb.set_ylabel(label)
axb.plot(psi_values, eta_values, label=label, color='C0', marker='s')
axb.set_ylim(0.0, 0.3)

lines, labels = ax.get_legend_handles_labels()
lines_b, labels_b = axb.get_legend_handles_labels()
ax.legend(lines + lines_b, labels + labels_b, frameon=False,
          loc='upper left')
fig.tight_layout()

if args.save_figures:
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'efficiency_compare_psi.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if args.show_figures:
    pyplot.show()
