"""Helper functions to load data digitized from Li & Dong (2016)."""

import numpy
import pathlib


DATADIR = pathlib.Path(__file__).absolute().parent / 'data'


def li_dong_2016_load_ct():
    """Load and return the thrust coefficient (digitized from Fig. 9).

    Returns
    -------
    numpy.ndarray
        Time values as a 1D array of floats.
    numpy.ndarray
        History of the thrust coefficient as a 1D array of floats.

    """
    filepath = DATADIR / 'li_dong_2016_fig9a.csv'
    with open(filepath, 'r') as infile:
        t, ct = numpy.loadtxt(infile, delimiter=',', unpack=True)
    return t, ct


def li_dong_2016_load_cl():
    """Load and return the lift coefficient (digitized from Fig. 9).

    Returns
    -------
    numpy.ndarray
        Time values as a 1D array of floats.
    numpy.ndarray
        History of the lift coefficient as a 1D array of floats.

    """
    filepath = DATADIR / 'li_dong_2016_fig9b.csv'
    with open(filepath, 'r') as infile:
        t, cl = numpy.loadtxt(infile, delimiter=',', unpack=True)
    return t, cl


def li_dong_2016_load_cz():
    """Load and return the spanwise coefficient (digitized from Fig. 9).

    Returns
    -------
    numpy.ndarray
        Time values as a 1D array of floats.
    numpy.ndarray
        History of the spanwise coefficient as a 1D array of floats.

    """
    filepath = DATADIR / 'li_dong_2016_fig9c.csv'
    with open(filepath, 'r') as infile:
        t, cz = numpy.loadtxt(infile, delimiter=',', unpack=True)
    return t, cz


def li_dong_2016_load_ux_profiles():
    """ Load and return the x-velocity profiles (digitized from Fig. 4a).

    Returns
    -------
    numpy.ndarray
        y positions as a 1D array of floats.
    numpy.ndarray
        x-velocity (relative to freestream speed, plus x position)
        as a 1D array of floats.

    """
    filepath = DATADIR / 'li_dong_2016_fig4a.csv'
    with open(filepath, 'r') as infile:
        ux, y = numpy.loadtxt(infile, delimiter=',', unpack=True)
    return ux, y


def li_dong_2016_load_uy_profiles():
    """ Load and return the y-velocity profiles (digitized from Fig. 4b).

    Returns
    -------
    numpy.ndarray
        y positions as a 1D array of floats.
    numpy.ndarray
        y-velocity (plus x position) as a 1D array of floats.

    """
    filepath = DATADIR / 'li_dong_2016_fig4b.csv'
    with open(filepath, 'r') as infile:
        uy, y = numpy.loadtxt(infile, delimiter=',', unpack=True)
    return uy, y


def li_dong_2016_load_uz_profiles():
    """ Load and return the z-velocity profiles (digitized from Fig. 4c).

    Returns
    -------
    numpy.ndarray
        z positions as a 1D array of floats.
    numpy.ndarray
        z-velocity (plus x position)
        as a 1D array of floats.

    """
    filepath = DATADIR / 'li_dong_2016_fig4c.csv'
    with open(filepath, 'r') as infile:
        uz, z = numpy.loadtxt(infile, delimiter=',', unpack=True)
    return uz, z

def li_dong_2016_load_kin_profiles():
    """ Load and return profiles of kinetic energy (digitized from Fig. 4d).

    Vertical profiles of the fluctuation of the kinetic energy at verious
    locations along x in the wake of the wing.

    Returns
    -------
    numpy.ndarray
        y positions as a 1D array of floats.
    numpy.ndarray
        fluctuation of the kinetic energy (plus x position)
        as a 1D array of floats.

    """
    filepath = DATADIR / 'li_dong_2016_fig4d.csv'
    with open(filepath, 'r') as infile:
        kin, y = numpy.loadtxt(infile, delimiter=',', unpack=True)
    return kin, y
