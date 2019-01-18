"""
Function to regularize a boundary points and obtain a uniform resolution.
"""

import math
import numpy


def get_perimeter(x, y):
    """
    Returns the perimeter of the geometry.
    """
    # Duplicate point if necessary to get a closed surface.
    atol = 1e-6
    if abs(x[0] - x[-1]) > atol or abs(y[0] - y[-1]) > atol:
        x, y = numpy.append(x, x[0]), numpy.append(y, y[0])
    return numpy.sum(numpy.sqrt((x[1:] - x[:-1])**2 + (y[1:] - y[:-1])**2))


def regularize(xo, yo, N=None, ds=None, atol=1.0E-06):
    """
    Regularize the geometry.

    Parameters
    ----------
    xo: numpy.ndarray of floats
        The x-coordinates of the boundary to regularize.
    yo: numpy.ndarray of floats
        The y-coordinates of the boundary to regularize.
    N: integer, optional
        Number of divisions;
        default: None.
    ds: float, optional
        Desired segment-length;
        default: None.
    atol: float, optional
        Desired tolerance for discretization;
        default: 1.0E-06.

    Returns
    -------
    x: numpy.ndarray of floats
        The x-coordinates of the regularized boundary.
    y: numpy.ndarray of floats
        The y-coordinates of the regularized boundary.
    """
    if not (N or ds):
        return
    if not N:
        N = int(math.ceil(get_perimeter(xo, yo) / ds))
    ds = get_perimeter(xo, yo) / N
    # Duplicate point if necessary to get a closed surface.
    if abs(xo[0] - xo[-1]) > atol or abs(yo[0] - yo[-1]) > atol:
        xo, yo = numpy.append(xo, xo[0]), numpy.append(yo, yo[0])
    # Regularize the geometry.
    next_idx = 1
    last_idx = xo.size - 1
    x, y = [xo[0]], [yo[0]]
    for i in range(1, N):
        xs, ys = x[-1], y[-1]  # Start point
        xe, ye = xo[next_idx], yo[next_idx]  # End point
        length = numpy.sqrt((xe - xs)**2 + (ye - ys)**2)
        if abs(ds - length) <= atol:  # Copy
            x.append(xe)
            y.append(ye)
            next_idx += 1
        elif ds < length:  # Interpolate between start and end points
            length2 = numpy.sqrt((xe - xs)**2 + (ye - ys)**2)
            x.append(xs + ds / length2 * (xe - xs))
            y.append(ys + ds / length2 * (ye - ys))
        else:  # Project the new point
            # Get segment index.
            while length < ds and next_idx < last_idx:
                next_idx += 1
                length = numpy.sqrt((xo[next_idx] - xs)**2 +
                                    (yo[next_idx] - ys)**2)
            xp, yp = xo[next_idx - 1], yo[next_idx - 1]
            xe, ye = xo[next_idx], yo[next_idx]
            # Interpolate on segment.
            precision = 1
            coeff = 0.0
            while abs(ds - length) > atol and precision < 6:
                xn, yn = xp + coeff * (xe - xp), yp + coeff * (ye - yp)
                length = numpy.sqrt((xn - xs)**2 + (yn - ys)**2)
                if length > ds:
                    coeff -= 0.1**precision
                    precision += 1
                coeff += 0.1**precision
            # Check new point not too close from first point before adding.
            length = numpy.sqrt((xn - x[0])**2 + (yn - y[0])**2)
            if length > 0.5 * ds:
                x.append(xn)
                y.append(yn)
    x, y = numpy.array(x), numpy.array(y)
    return x, y
