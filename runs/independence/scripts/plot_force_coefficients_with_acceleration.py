"""Plot the instantaneous force coefficients and compare with/without acc."""

from matplotlib import pyplot
import numpy
import pathlib

import petibmpy

import rodney


def get_acceleration(t, config):
    """Compute the components of the acceleration of the center of mass."""
    # Compute history of the rolling and pitching angle.
    phi = config.rolling(t)
    theta = config.pitching(t)
    # Compute history of the angular velocities.
    phi_dot = config.rolling_angular_velocity(t)
    theta_dot = config.pitching_angular_velocity(t)
    # Compute history of the angular accelerations.
    phi_dot_dot = config.rolling_angular_acceleration(t)
    theta_dot_dot = config.pitching_angular_acceleration(t)

    x0, y0, z0 = 0.0, 0.0, config.S / 2  # center of mass
    xc, yc, zc = 0.0, 0.0, 0.0  # hinge (fixed point)

    # Compute the history of the location of the center.
    x, y, z = numpy.empty_like(t), numpy.empty_like(t), numpy.empty_like(t)
    for i, ti in enumerate(t):
        phi_i = config.rolling(ti)
        theta_i = config.pitching(ti)
        point = rodney.rotation(x0, y0, z0,
                                roll=phi_i, pitch=theta_i,
                                center=(xc, yc, zc))
        x[i], y[i], z[i] = point

    # Compute the components of the acceleration.
    a_x = (theta_dot_dot * numpy.cos(phi) * (y - yc) -
            theta_dot_dot * numpy.sin(phi) * (z - zc))

    a_y = (-theta_dot_dot * numpy.cos(phi) * (x - xc) -
           theta_dot**2 * numpy.cos(phi) * (numpy.cos(phi) * (y - yc) -
                                            numpy.sin(phi) * (z - zc)) +
           phi_dot_dot * (z - zc) - phi_dot**2 * (y - yc) +
           2 * theta_dot * phi_dot * numpy.sin(phi) * (x - xc))

    a_z = (theta_dot_dot * numpy.sin(phi) * (x - xc) +
           theta_dot**2 * numpy.sin(phi) * (numpy.cos(phi) * (y - yc) -
                                            numpy.sin(phi) * (z - zc)) -
           phi_dot_dot * (y - yc) - phi_dot**2 * (z - zc) +
           2 * theta_dot * phi_dot * numpy.cos(phi) * (x - xc))

    return a_x, a_y, a_z


def load_force_coefficients_with_acc(filepath, config):
    """"Load forces and compute force coefficients with inertial term."""
    # Load forces from file.
    t, fx, fy, fz = petibmpy.read_forces(filepath)
    # Add inertial term to forces.
    a_x, a_y, a_z = get_acceleration(t, config)
    V = 0.03 * config.A_plan  # disk volume
    fx += config.rho * V * a_x
    fy += config.rho * V * a_y
    fz += config.rho * V * a_z
    # Drag to thrust.
    fx *= -1.0
    # Convert forces to force coefficients.
    coeff = 1 / (0.5 * config.rho * config.U_inf**2 * config.A_plan)
    ct, cl, cz = petibmpy.get_force_coefficients(fx, fy, fz, coeff=coeff)
    # Return solution.
    return rodney.Solution(t=t / config.T, ct=ct, cl=cl, cz=cz)


args = rodney.parse_command_line()
maindir = pathlib.Path(__file__).absolute().parents[1]

# Load force coefficients for simulation with flat plate.
label1 = 'Flat plate'
simudir1 = maindir / 'run3'
config1 = rodney.WingKinematics(nt_period=1000)
filepath = simudir1 / 'output' / 'forces-0.txt'
solution1 = rodney.load_force_coefficients(filepath, config1)
rodney.print_stats(label1, *rodney.get_stats(solution1, limits=(3, 5)))
plot_kwargs1 = dict(linestyle='-', color='C0')  # plot keyword arguments

# Load force coefficients for simulation with disk (3% thickness).
label2 = 'Disk (%3 thickness)'
simudir2 = maindir / 'run3-disk'
config2 = rodney.WingKinematics(nt_period=1000)
filepath = simudir2 / 'output' / 'forces-0.txt'
solution2 = rodney.load_force_coefficients(filepath, config2)
rodney.print_stats(label2, *rodney.get_stats(solution2, limits=(3, 5)))
plot_kwargs2 = dict(linestyle='-', color='C3')  # plot keyword arguments

# Load force coefficients for simulation with disk and with inertial term.
label3 = 'Disk (with inertial term)'
simudir3 = maindir / 'run3-disk'
config3 = rodney.WingKinematics(nt_period=1000)
filepath = simudir3 / 'output' / 'forces-0.txt'
solution3 = load_force_coefficients_with_acc(filepath, config3)
rodney.print_stats(label3, *rodney.get_stats(solution3, limits=(3, 5)))
plot_kwargs3 = dict(linestyle='--', color='black')  # plot keyword arguments

# Plot the history of the force coefficients.
pyplot.rc('font', family='serif', size=12)
fig, (ax1, ax2, ax3) = pyplot.subplots(ncols=3, figsize=(12.0, 3.0))
xlim, ylim = (3.0, 5.0), (-6.0, 6.0)
# Plot the history of the thrust coefficient.
ax1.set_xlabel('$t / T$')
ax1.set_ylabel('$C_T$')
ax1.plot(solution1.t, solution1.ct, label=label1, **plot_kwargs1)
ax1.plot(solution2.t, solution2.ct, label=label2, **plot_kwargs2)
ax1.plot(solution3.t, solution3.ct, label=label3, **plot_kwargs3)
ax1.set_xlim(xlim)
ax1.set_ylim(ylim)
# Plot the history of the lift coefficient.
ax2.set_xlabel('$t / T$')
ax2.set_ylabel('$C_L$')
ax2.plot(solution1.t, solution1.cl, label=label1, **plot_kwargs1)
ax2.plot(solution2.t, solution2.cl, label=label2, **plot_kwargs2)
ax2.plot(solution3.t, solution3.cl, label=label3, **plot_kwargs3)
ax2.set_xlim(xlim)
ax2.set_ylim(ylim)
# Plot the history of the spanwise force coefficient.
ax3.set_xlabel('$t / T$')
ax3.set_ylabel('$C_Z$')
ax3.plot(solution1.t, solution1.cz, label=label1, **plot_kwargs1)
ax3.plot(solution2.t, solution2.cz, label=label2, **plot_kwargs2)
ax3.plot(solution3.t, solution3.cz, label=label3, **plot_kwargs3)
ax3.set_xlim(xlim)
ax3.set_ylim(ylim)

if args.extra_data:
    # Add the force coefficients from Li and Dong (2016).
    # The signals were digitized from Figure 9 of the article.
    scatter_kwargs = dict(s=10, facecolors='none', edgecolors='black')
    ax1.scatter(*rodney.li_dong_2016_load_ct(), label='Li & Dong (2016)',
                **scatter_kwargs)
    ax2.scatter(*rodney.li_dong_2016_load_cl(), label='Li & Dong (2016)',
                **scatter_kwargs)
    ax3.scatter(*rodney.li_dong_2016_load_cz(), label='Li & Dong (2016)',
                **scatter_kwargs)

ax1.legend(frameon=False, prop=dict(size=10))
fig.tight_layout()

if args.save_figures:
    figdir = maindir / 'figures'
    figdir.mkdir(parents=True, exist_ok=True)
    filepath = figdir / 'force_coefficients_with_acceleration.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

if args.show_figures:
    pyplot.show()
