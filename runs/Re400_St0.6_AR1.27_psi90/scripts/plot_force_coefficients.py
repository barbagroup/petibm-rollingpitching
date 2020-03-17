"""Plot the instantaneous force coefficients."""

import math
from matplotlib import pyplot
import numpy
import pathlib

import petibmpy

import rodney

from kinematics import rolling, pitching
from kinematics import rho, U_inf, A_plan, T, A_phi, A_theta, psi, f


args = rodney.parse_command_line()
display_kinematics = False  # Add kinematics to the figure

# Load forces from file.
simudir = pathlib.Path(__file__).absolute().parents[1]
datadir = simudir / 'output'
filepath = datadir / 'forces-0.txt'
t, fx, fy, fz = petibmpy.read_forces(filepath)
fx = -fx

# Convert forces to force coefficients.
coeff = 1 / (0.5 * rho * U_inf**2 * A_plan)
ct, cl, cz = petibmpy.get_force_coefficients(fx, fy, fz, coeff=coeff)

# Compute the time-averaged force coefficients and RMS.
limits = (3 * T, 5 * T)
ct_mean, cl_mean, cz_mean = petibmpy.get_time_averaged_values(t, ct, cl, cz,
                                                              limits=limits)
ct_rms, cl_rms, cz_rms = petibmpy.get_rms_values(t, ct, cl, cz,
                                                 limits=limits)
print(f'<C_T> = {ct_mean:.3f}, (C_T)_rms = {ct_rms:.3f}')
print(f'<C_L> = {cl_mean:.3f}, (C_L)_rms = {cl_rms:.3f}')
print(f'<C_Z> = {cz_mean:.3f}, (C_Z)_rms = {cz_rms:.3f}')

# Plot the history of the force coefficients.
pyplot.rc('font', family='serif', size=12)
fig, (ax1, ax2, ax3) = pyplot.subplots(ncols=3, figsize=(12.0, 3.0))
xlim, ylim = (3.0, 5.0), (-6.0, 6.0)
# Plot the history of the thrust coefficient.
ax1.set_xlabel('$t / T$')
ax1.set_ylabel('$C_T$')
ax1.plot(t / T, ct, label='PetIBM')
ax1.axhline(ct_mean, color='C3', linestyle='-')
ax1.set_xlim(xlim)
ax1.set_ylim(ylim)
# Plot the history of the lift coefficient.
ax2.set_xlabel('$t / T$')
ax2.set_ylabel('$C_L$')
ax2.plot(t / T, cl, label='PetIBM')
ax2.axhline(cl_mean, color='C3', linestyle='-')
ax2.set_xlim(xlim)
ax2.set_ylim(ylim)
# Plot the history of the spanwise force coefficient.
ax3.set_xlabel('$t / T$')
ax3.set_ylabel('$C_Z$')
ax3.plot(t / T, cz, label='PetIBM')
ax3.axhline(cz_mean, color='C3', linestyle='-')
ax3.set_xlim(xlim)
ax3.set_ylim(ylim)

if display_kinematics:
    # Add the rolling and pitching kinematics to the figure.
    for ax in (ax1, ax2, ax3):
        axt = ax.twinx()
        axt.set_ylabel('Plate Rotation ($^o$)')
        axt.plot(t / T, numpy.degrees(rolling(t, A_phi, f)),
                 label='Rolling', color='black', linestyle='--')
        axt.plot(t / T, numpy.degrees(pitching(t, A_theta, f, psi)),
                 label='Pitching', color='black', linestyle=':')
        axt.set_xlim(xlim)
        axt.set_ylim(-60.0, 60.0)

if args.extra_data:
    # Add the force coefficients from Li and Dong (2016).
    # The signals were digitized from Figure 9 of the article.
    ax1.plot(*rodney.li_dong_2016_load_ct(), label='Li & Dong (2016)')
    ax2.plot(*rodney.li_dong_2016_load_cl(), label='Li & Dong (2016)')
    ax3.plot(*rodney.li_dong_2016_load_cz(), label='Li & Dong (2016)')

ax1.legend(prop={'size': 10}, frameon=False)
fig.tight_layout()

if args.save_figures:
    figdir = simudir / 'figures'
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'force_coefficients.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if args.show_figures:
    pyplot.show()
