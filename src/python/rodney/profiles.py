"""Functions to load solution from volume probes and interpolate profiles."""

import numpy

import petibmpy


def get_vertical_profile_xy(filepath, name, time, xloc, zloc):
    """Return the profile along the y direction at given x and z locations.

    The function loads the solution of from the volume probe at a given time.
    The solution is first interpolated along the z direction and then,
    along the x direction.

    Parameters
    ----------
    filepath : pathlib.Path
        Path of the file with the volume probe data.
    name : str
        Name of the variable to load.
    time : float
        Time value at which to load the data.
    xloc : float
        Location along the x direction at which to interpolate data.
    zloc : float
        Location along the z direction at which to interpolate data.

    Returns
    -------
    numpy.ndarray
        y locations along the profile as a 1D array of floats.
    numpy.ndarray
        Values of the interpolated variable as a 1D array of floats.

    """
    probe = petibmpy.ProbeVolume(name, name)
    (x, y, z), u = probe.read_hdf5(filepath, time)
    u = petibmpy.linear_interpolation(u, z, zloc)
    u = numpy.swapaxes(u, 0, 1)
    u = petibmpy.linear_interpolation(u, x, xloc)
    assert y.size == u.size
    return y, u


def get_spanwise_profile_xz(filepath, name, time, xloc, yloc):
    """Return the profile along the z direction at given x and y locations.

    The function loads the solution of from the volume probe at a given time.
    The solution is first interpolated along the y direction and then,
    along the x direction.

    Parameters
    ----------
    filepath : pathlib.Path
        Path of the file with the volume probe data.
    name : str
        Name of the variable to load.
    time : float
        Time value at which to load the data.
    xloc : float
        Location along the x direction at which to interpolate data.
    yloc : float
        Location along the y direction at which to interpolate data.

    Returns
    -------
    numpy.ndarray
        z locations along the profile as a 1D array of floats.
    numpy.ndarray
        Values of the interpolated variable as a 1D array of floats.

    """
    probe = petibmpy.ProbeVolume(name, name)
    (x, y, z), u = probe.read_hdf5(filepath, time)
    u = numpy.swapaxes(u, 0, 1)
    u = petibmpy.linear_interpolation(u, y, yloc)
    u = numpy.swapaxes(u, 0, 1)
    u = petibmpy.linear_interpolation(u, x, xloc)
    assert z.size == u.size
    return z, u
