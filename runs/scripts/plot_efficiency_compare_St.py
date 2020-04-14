"""Plot the propulsive efficiency and cycle-averaged trust coefficient.

Plot agains the Strouhal number.
"""

from matplotlib import pyplot
import numpy
import pathlib

import rodney


args = rodney.parse_command_line()
maindir = pathlib.Path(__file__).absolute().parents[1]
figdir = maindir / 'figures'

# Hard-coded for now.
St_values = [0.4, 0.6, 0.8, 1.0, 1.2]
ct_values = [-0.0614, 0.9138, 2.5538, 4.8801, 7.9053]
eta_values = [-0.0493, 0.1635, 0.1705, 0.1552, 0.1384]

pyplot.rc('font', family='serif', size=14)
fig, ax = pyplot.subplots(figsize=(6.0, 4.0))
# Plot cycle-averaged thrust coefficient versus Strouhal number.
ax.set_xlabel('St')
label = r'$\bar{C_T}$'
ax.set_ylabel(label)
ax.plot(St_values, ct_values, label=label, color='C3', marker='o')
ax.set_ylim(-2.0, 12.0)
# Plot cycle-averaged propulsive efficiency versus Strouhal number.
axb = ax.twinx()
label = r'$\eta$'
axb.set_ylabel(label)
axb.plot(St_values, eta_values, label=label, color='C0', marker='s')
axb.set_ylim(-0.05, 0.3)

lines, labels = ax.get_legend_handles_labels()
lines_b, labels_b = axb.get_legend_handles_labels()
ax.legend(lines + lines_b, labels + labels_b, frameon=False)
fig.tight_layout()

if args.save_figures:
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'efficiency_compare_St.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if args.show_figures:
    pyplot.show()
