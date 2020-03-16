"""Functions to process forces and forces coefficients."""

import collections
import numpy

import petibmpy


Solution = collections.namedtuple('Solution', ['t', 'ct', 'cl', 'cz'])
Stats = collections.namedtuple('Stats', ['ct', 'cl', 'cz'])


def load_force_coefficients(filepath, config):
    """Load forces from file and return force coefficients."""
    # Load forces from file.
    t, fx, fy, fz = petibmpy.read_forces(filepath)
    fx *= -1.0  # drag to thrust
    # Convert forces to force coefficients.
    rho, U_inf, A_plan = (getattr(config, name)
                          for name in ('rho', 'U_inf', 'A_plan'))
    coeff = 1 / (0.5 * rho * U_inf**2 * A_plan)
    # Non-dimensionalize time values by period.
    t /= config.T
    ct, cl, cz = petibmpy.get_force_coefficients(fx, fy, fz, coeff=coeff)
    return Solution(t=t, ct=ct, cl=cl, cz=cz)


def get_stats(solution, limits=(0, numpy.infty)):
    """Compute mean and rms values of the force coefficients."""
    means = Stats(*petibmpy.get_time_averaged_values(*solution, limits=limits))
    rms = Stats(*petibmpy.get_rms_values(*solution, limits=limits))
    return means, rms


def print_stats(label, means, rms, ndigits=3):
    """Print statistics about the force coefficients."""
    def r(v):
        return round(v, ndigits=ndigits)
    print(f'\n{label}:')
    print(f'<C_T> = {r(means.ct)}, (C_T)_rms = {r(rms.ct)}')
    print(f'<C_L> = {r(means.cl)}, (C_L)_rms = {r(rms.cl)}')
    print(f'<C_Z> = {r(means.cz)}, (C_Z)_rms = {r(rms.cz)}')
