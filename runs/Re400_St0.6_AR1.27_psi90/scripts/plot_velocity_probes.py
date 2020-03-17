"""Plot the velocity profile at certain location along the x-direction."""

import h5py
from matplotlib import pyplot
import numpy
import pathlib
import yaml

import petibmpy

import rodney

from kinematics import U_inf, S


args = rodney.parse_command_line()

simudir = pathlib.Path(__file__).absolute().parents[1]
datadir = simudir / 'output'
time = 6.528332  # data over the last cycle
xlocs = [1.0, 2.0, 3.0, 4.0, 5.0]

if args.save_figures:
    figdir = simudir / 'figures'
    figdir.mkdir(parents=True, exist_ok=True)

name = 'u'
pyplot.rc('font', family='serif', size=14)
fig, ax = pyplot.subplots(figsize=(6.0, 6.0))
ax.set_xlabel('x/c')
ax.set_ylabel('y/c')
ax.axhline(0.0, color='black', linestyle='--')
for i, xi in enumerate(xlocs):
    filepath = datadir / 'probe{}-{}.h5'.format(i + 1, name)
    probe = petibmpy.ProbeVolume(name, name)
    (x, y, z), u = probe.read_hdf5(filepath, time)
    u = petibmpy.linear_interpolation(u, z, S / 2)
    u = numpy.swapaxes(u, 0, 1)
    u = petibmpy.linear_interpolation(u, x, xi)
    ax.plot(xi + u - U_inf, y)
if args.extra_data:
    ax.scatter(*rodney.li_dong_2016_load_ux_profiles(),
               marker='o', edgecolor='black', color='none')
ax.set_xlim(-2.0, 6.0)
ax.set_ylim(-3.0, 3.0)
fig.tight_layout()
if args.save_figures:
    filepath = figdir / 'ux_profiles.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

name = 'v'
fig, ax = pyplot.subplots(figsize=(6.0, 6.0))
ax.set_xlabel('x/c')
ax.set_ylabel('y/c')
ax.axhline(0.0, color='black', linestyle='--')
for i, xi in enumerate(xlocs):
    filepath = datadir / 'probe{}-{}.h5'.format(i + 1, name)
    probe = petibmpy.ProbeVolume(name, name)
    (x, y, z), v = probe.read_hdf5(filepath, time)
    v = petibmpy.linear_interpolation(v, z, S / 2)
    v = numpy.swapaxes(v, 0, 1)
    v = petibmpy.linear_interpolation(v, x, xi)
    ax.plot(xi + v, y)
if args.extra_data:
    ax.scatter(*rodney.li_dong_2016_load_uy_profiles(),
               marker='o', edgecolor='black', color='none')
ax.set_xlim(-2.0, 6.0)
ax.set_ylim(-3.0, 3.0)
fig.tight_layout()
if args.save_figures:
    filepath = figdir / 'uy_profiles.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

name = 'w'
fig, ax = pyplot.subplots(figsize=(6.0, 6.0))
ax.set_xlabel('x/c')
ax.set_ylabel('z/c')
ax.axhline(0.0, color='black', linestyle='--')
for i, xi in enumerate(xlocs):
    filepath = datadir / 'probe{}-{}.h5'.format(i + 1, name)
    probe = petibmpy.ProbeVolume(name, name)
    (x, y, z), w = probe.read_hdf5(filepath, time)
    w = numpy.swapaxes(w, 0, 1)
    w = petibmpy.linear_interpolation(w, y, 0.0)
    w = numpy.swapaxes(w, 0, 1)
    w = petibmpy.linear_interpolation(w, x, xi)
    ax.plot(xi + w, z - S / 2)
if args.extra_data:
    ax.scatter(*rodney.li_dong_2016_load_uz_profiles(),
               marker='o', edgecolor='black', color='none')
ax.set_xlim(-2.0, 6.0)
ax.set_ylim(-2.0, 2.0)
fig.tight_layout()
if args.save_figures:
    filepath = figdir / 'uz_profiles.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if args.show_figures:
    pyplot.show()
