"""Plot the velocity profile at certain location along the x-direction."""

import h5py
from matplotlib import pyplot
import numpy
import pathlib
import yaml

import petibmpy

import rodney


args = rodney.parse_command_line()

config = rodney.WingKinematics(psi=120.0, Re=200, St=0.6, nt_period=2000)
simudir = pathlib.Path(__file__).absolute().parents[1]
datadir = simudir / 'output'
time = round(config.tf, ndigits=6)  # final time value
xlocs = [1.0, 2.0, 3.0, 4.0, 5.0]

if args.save_figures:
    figdir = simudir / 'figures'
    figname_suffix = ''
    figdir.mkdir(parents=True, exist_ok=True)

name = 'u'
pyplot.rc('font', family='serif', size=14)
fig, ax = pyplot.subplots(figsize=(6.0, 6.0))
ax.set_xlabel('x/c')
ax.set_ylabel('y/c')
ax.axhline(0.0, color='black', linestyle='--')
zloc = config.S / 2
for i, xloc in enumerate(xlocs):
    filepath = datadir / 'probe{}-{}.h5'.format(i + 1, name)
    y, u = rodney.get_vertical_profile_xy(filepath, name, time, xloc, zloc)
    ax.plot(xloc + u - config.U_inf, y)
ax.set_xlim(-2.0, 6.0)
ax.set_ylim(-3.0, 3.0)
fig.tight_layout()
if args.save_figures:
    filepath = figdir / f'ux_profiles{figname_suffix}.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

name = 'v'
fig, ax = pyplot.subplots(figsize=(6.0, 6.0))
ax.set_xlabel('x/c')
ax.set_ylabel('y/c')
ax.axhline(0.0, color='black', linestyle='--')
zloc = config.S / 2
for i, xloc in enumerate(xlocs):
    filepath = datadir / 'probe{}-{}.h5'.format(i + 1, name)
    y, v = rodney.get_vertical_profile_xy(filepath, name, time, xloc, zloc)
    ax.plot(xloc + v, y)
ax.set_xlim(-2.0, 6.0)
ax.set_ylim(-3.0, 3.0)
fig.tight_layout()
if args.save_figures:
    filepath = figdir / f'uy_profiles{figname_suffix}.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

name = 'w'
fig, ax = pyplot.subplots(figsize=(6.0, 6.0))
ax.set_xlabel('x/c')
ax.set_ylabel('z/c')
ax.axhline(0.0, color='black', linestyle='--')
yloc = 0.0
for i, xloc in enumerate(xlocs):
    filepath = datadir / 'probe{}-{}.h5'.format(i + 1, name)
    z, w = rodney.get_spanwise_profile_xz(filepath, name, time, xloc, yloc)
    ax.plot(xloc + w, z - config.S / 2)
ax.set_xlim(-2.0, 6.0)
ax.set_ylim(-2.0, 2.0)
fig.tight_layout()
if args.save_figures:
    filepath = figdir / f'uz_profiles{figname_suffix}.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if args.show_figures:
    pyplot.show()
