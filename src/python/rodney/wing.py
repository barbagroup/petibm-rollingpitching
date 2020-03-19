"""Kinematics of the rolling-pitching wing."""

import math
import numpy
from scipy.spatial import ConvexHull

import distmesh
import petibmpy


def rolling(t, A, f):
    """Return the instantaneous rolling angle.

    Parameters
    ----------
    t : float
        Time.
    A : float
        Rolling amplitude.
    f : float
        Frequency.

    Returns
    -------
    phi : float
        Rolling angle (in radians).

    """
    phi = -A * numpy.cos(2 * numpy.pi * f * t)
    return phi


def pitching(t, A, f, psi, bias=0.0):
    """Return the instantaneous pitching angle.

    Parameters
    ----------
    t : float
        Time.
    A : float
        Pitching amplitude.
    f : float
        Frequency.
    psi : float
        Phase difference (in radians) between pitching and rolling.
    bias : float (optional)
        Static pitching bias angle (in radians); default: 0.0.

    Returns
    -------
    theta : float
        Pitching angle (in radians).

    """
    theta = -A * numpy.cos(2 * numpy.pi * f * t + psi) + bias
    return theta


def rolling_angular_velocity(t, A, f):
    """Return the instantaneous rolling angular velocity.

    Parameters
    ----------
    t : float
        Time.
    A : float
        Rolling amplitude.
    f : float
        Frequency.

    Returns
    -------
    float
        Angular velocity.

    """
    w = 2 * numpy.pi * f
    phi_dot = w * A * numpy.sin(w * t)
    return phi_dot


def pitching_angular_velocity(t, A, f, psi):
    """Return the instantaneous pitching angular velocity.

    Parameters
    ----------
    t : float
        Time.
    A : float
        Pitching amplitude.
    f : float
        Frequency.
    psi : float
        Phase difference (in radians) between pitching and rolling.

    Returns
    -------
    float
        Angular velocity.

    """
    w = 2 * numpy.pi * f
    theta_dot = w * A * numpy.sin(w * t + psi)
    return theta_dot


def rolling_angular_acceleration(t, A, f):
    w = 2 * numpy.pi * f
    phi_dot_dot = w**2 * A * numpy.cos(w * t)
    return phi_dot_dot


def pitching_angular_acceleration(t, A, f, psi):
    w = 2 * numpy.pi * f
    theta_dot_dot = w**2 * A * numpy.cos(w * t + psi)
    return theta_dot_dot


class WingKinematics(object):

    def __init__(self, c=1.0, AR=1.27, hook=[0.0, 0.0, 0.0],
                 A_phi=45.0, A_theta=45.0, psi=90.0, theta_bias=0.0,
                 Re=200.0, U_inf=1.0, rho=1.0,
                 St=0.6, n_periods=5, nt_period=2000):
        """Set parameters of the kinematics."""
        # Geometrical parameters.
        self.c = c  # chord length
        self.AR = AR  # aspect ratio (AR = 1.27 --> S / c = 1)
        self.S = numpy.pi * c * AR / 4  # span
        self.A_plan = numpy.pi * c * self.S / 4
        self.R_avg = self.S / 2  # average rotational radius
        self.hook = hook  # center of rotation

        # Fluid properties.
        self.U_inf = U_inf  # freestream velocity
        self.Re = Re  # Reynolds number
        self.nu = U_inf * c / Re  # kinematic viscosity
        self.rho = rho  # density

        # Rolling parameters.
        self.A_phi = numpy.radians(A_phi)  # rolling amplitude

        # Pitching parameters.
        self.A_theta = numpy.radians(A_theta)  # pitching amplitude
        self.psi = numpy.radians(psi)  # phase difference
        self.theta_bias = numpy.radians(theta_bias)  # static pitching bias

        # Temporal parameters.
        self.St = St  # Strouhal number
        _A = self.A_phi if self.A_phi > 1e-6 else self.A_theta
        self.f = St * U_inf / (2 * _A * self.R_avg)  # frequency
        self.T = 1 / self.f  # time period

        # Simulation parameters.
        self.n_periods = n_periods  # number of periods
        self.tf = n_periods * self.T  # final time
        self.nt_period = nt_period  # number of time steps per period
        self.nt = n_periods * nt_period  # number of time steps
        self.dt = self.tf / self.nt  # time-step size

    def __repr__(self):
        """Set object representation."""
        return ('Kinematics:\n'
                f'- chord length: c = {self.c}\n'
                f'- span length: S = {self.S}\n'
                f'- aspect ratio: AR = {self.AR}\n'
                f'- planform area: A_plan = {self.A_plan}\n'
                f'- avg. rot. radius: R_avg = {self.R_avg}\n'
                f'- center of rotation: CoR = {self.hook}\n'
                f'- freestream speed: U_inf = {self.U_inf}\n'
                f'- Reynolds number: Re = {self.Re}\n'
                f'- kinematic viscosity: nu = {self.nu}\n'
                f'- fluid density: rho = {self.rho}\n'
                f'- rolling amplitude: A_phi = {self.A_phi}\n'
                f'- pitching amplitude: A_theta = {self.A_theta}\n'
                f'- phase difference: psi = {self.psi}\n'
                f'- pitching bias: theta_bias = {self.theta_bias}\n'
                f'- Strouhal number: St = {self.St}\n'
                f'- flapping frequency: f = {self.f}\n'
                f'- flapping period: T = {self.T}\n'
                f'- number of periods: n_periods = {self.n_periods}\n'
                f'- final time: tf = {self.tf}\n'
                f'- time steps / period: nt_period = {self.nt_period}\n'
                f'- time steps: nt = {self.nt}\n'
                f'- time-step size: dt = {self.dt}\n')

    def set_coordinates(self, x, y, z, org=False):
        self.x, self.y, self.z = x, y, z
        self.size = x.size
        if org:
            self.x0, self.y0, self.z0 = x.copy(), y.copy(), z.copy()

    def get_coordinates(self, org=False):
        if org:
            return self.x0, self.y0, self.z0
        return self.x, self.y, self.z

    def create_body(self, ds=0.05, thickness=0.0, sort_points=False):
        a, b = self.c / 2, self.S / 2
        center = (self.hook[0], self.hook[-1] + b)
        if thickness > 0.0:
            # Create a thick ellipse.
            x, y, z = create_disk(thickness * self.c, a, b,
                                  center=center, ds=ds)
        else:
            # Create flat plate (ellipse).
            x, z = create_ellipse(a, b, center=center, ds=ds)
            y = numpy.zeros_like(x)
        if sort_points:
            # Re-order points
            idx = numpy.argmin(z)
            x_ref, z_ref = x[idx], z[idx]
            dist = numpy.sqrt((x - x_ref)**2 + (z - z_ref)**2)
            indices = numpy.argsort(dist)
            x, y, z = x[indices], y[indices], z[indices]
        self.set_coordinates(x, y, z, org=True)

    def load_body(self, filepath, **kwargs):
        x, y, z = petibmpy.read_body(filepath, **kwargs)
        self.set_coordinates(x, y, z, org=True)

    def rolling(self, t):
        return rolling(t, self.A_phi, self.f)

    def pitching(self, t):
        return pitching(t, self.A_theta, self.f, self.psi,
                        bias=self.theta_bias)

    def rolling_angular_velocity(self, t):
        return rolling_angular_velocity(t, self.A_phi, self.f)

    def pitching_angular_velocity(self, t):
        return pitching_angular_velocity(t, self.A_theta, self.f, self.psi)

    def rolling_angular_acceleration(self, t):
        return rolling_angular_acceleration(t, self.A_phi, self.f)

    def pitching_angular_acceleration(self, t):
        return pitching_angular_acceleration(t, self.A_theta, self.f, self.psi)

    def compute_position(self, t):
        roll = self.rolling(t)
        pitch = self.pitching(t)
        return vrotation(self.x0, self.y0, self.z0,
                         roll=roll, yaw=0.0, pitch=pitch,
                         center=self.hook)

    def get_normal(self):
        a = numpy.array([self.x[0], self.y[0], self.z[0]])
        b = numpy.array([self.x[1], self.y[1], self.z[1]])
        c = numpy.array([self.x[2], self.y[2], self.z[2]])
        v1 = (a - b) / numpy.linalg.norm(a - b)
        v2 = (c - a) / numpy.linalg.norm(c - a)
        v3 = numpy.cross(v1, v2)
        return v3 / numpy.linalg.norm(v3)

    def update_position(self, t):
        self.x, self.y, self.z = self.compute_position(t)
        self.n = self.get_normal()

    def compute_velocity(self, t):
        phi = self.rolling(t)
        phi_dot = self.rolling_angular_velocity(t)
        theta_dot = self.pitching_angular_velocity(t)
        xc, yc, zc = self.hook
        ux = -theta_dot * (numpy.sin(phi) * (self.z - zc) -
                           numpy.cos(phi) * (self.y - yc))
        uy = (-theta_dot * numpy.cos(phi) * (self.x - xc) +
              phi_dot * (self.z - zc))
        uz = (+theta_dot * numpy.sin(phi) * (self.x - xc) -
              phi_dot * (self.y - yc))
        return ux, uy, uz

    def get_velocity(self):
        return self.ux, self.uy, self.uz

    def update_velocity(self, t):
        self.ux, self.uy, self.uz = self.compute_velocity(t)


def create_ellipse(a, b, center=(0.0, 0.0), ds=0.05):
    """Create discretized ellipse.

    Parameters
    ----------
    a : float
        Semi major axis of the ellipse.
    b : float
        Semi major axis of the ellipse.
    center : tuple of floats, optional
        Center of the ellipse; default is (0.0, 0.0).
    ds : float, optional
        Resolution of the ellipse (approx. distance between two neighbors);
        default is 0.05.

    Returns
    -------
    numpy.ndarray
        x-coordinate of points on ellipse as a 1D array of floats.
    numpy.ndarray
        y-coordinate of points on ellipse as a 1D array of floats.

    """
    xc, yc = center
    # Create distance function.
    fd = lambda p: ((p[:, 0] - xc)**2 / a**2 +
                    (p[:, 1] - yc)**2 / b**2 - 1)

    # Discretize the ellipse.
    bbox = (xc - a, yc - b, xc + a, yc + b)  # bounding box
    p, _ = distmesh.distmesh2d(fd, distmesh.huniform, ds, bbox, fig=None)

    # Store point coordinates in arrays.
    x, y = p[:, 0], p[:, 1]

    return x, y


def create_disk(thickness, a, b, center=(0.0, 0.0), ds=0.05):
    """Create a disk of specified thickness with elliptical surface.

    Parameters
    ----------
    thickness : float
        Thickness of the disk.
    a : float
        Semi major axis of the ellipse.
    b : float
        Semi major axis of the ellipse.
    center : tuple of floats, optional
        Center of the ellipse; default is (0.0, 0.0).
    ds : float, optional
        Resolution of the ellipse (approx. distance between two neighbors);
        default is 0.05.

    Returns
    -------
    numpy.ndarray
        x-coordinates of the disk points as a 1D array of floats.
    numpy.ndarray
        y-coordinates of the disk points as a 1D array of floats.
    numpy.ndarray
        z-coordinates of the disk points as a 1D array of floats.

    """
    # Create ellipse (flat plate).
    x0, z0 = create_ellipse(a, b, center=center, ds=ds)
    # Limits of the disk.
    ystart, yend = -0.5 * thickness, 0.5 * thickness
    # Store coordinates of bottom surface.
    xb, zb = x0.copy(), z0.copy()
    yb = numpy.full_like(xb, ystart)
    # Store coordinates of top surface.
    xt, zt = x0.copy(), z0.copy()
    yt = numpy.full_like(xt, yend)
    # Get coordinates of contour points from bottom.
    points = numpy.array([xb, zb]).T
    hull = ConvexHull(points)
    xc, zc = points[hull.vertices, 0], points[hull.vertices, 1]
    # Generate points on lateral side of the disk.
    tol = 1e-8  # tolerance to beat machine precision error for math.ceil
    N = math.ceil(thickness / ds - tol) - 1  # number of lateral points
    if N > 0:
        ds_true = thickness / (N + 1)  # adjust spacing for uniform split
        xl, zl = numpy.tile(xc, N), numpy.tile(zc, N)
        yl = [numpy.full_like(xc, ystart + (n + 1) * ds_true)
              for n in range(N)]
        yl = numpy.concatenate(yl)
    else:
        # No points on lateral side of disk.
        xl, yl, zl = numpy.array([]), numpy.array([]), numpy.array([])
    # Concatenate bottom, top, and lateral surfaces.
    x = numpy.concatenate([xb, xt, xl])
    y = numpy.concatenate([yb, yt, yl])
    z = numpy.concatenate([zb, zt, zl])
    return x, y, z

def rotation(x, y, z,
             roll=0.0, yaw=0.0, pitch=0.0, center=[0.0, 0.0, 0.0]):
    """Rotate point.

    Parameters
    ----------
    x : float
        x-coordinate of point.
    y : float
        y-coordinate of point.
    z : float
        z-coordinate of point.
    roll : float (optional)
        Roll angle (in radians); default: 0.0.
    yaw : float (optional)
        Yaw angle (in radians); default: 0.0.
    pitch : float (optional)
        Pitch angle (in radians); default: 0.0.
    center : list of floats
        Coordinates of the center of rotation;
        default: [0.0, 0.0, 0.0].

    Returns
    -------
    float
        x-coordinate of rotated point.
    float
        y-coordinate of rotated point.
    float
        z-coordinate of rotated point.

    """
    center = numpy.array(center)
    Rx = numpy.array([[1.0, 0.0, 0.0],
                      [0.0, math.cos(roll), math.sin(roll)],
                      [0.0, -math.sin(roll), math.cos(roll)]])
    Ry = numpy.array([[math.cos(yaw), 0.0, math.sin(yaw)],
                      [0.0, 1.0, 0.0],
                      [-math.sin(yaw), 0.0, math.cos(yaw)]])
    Rz = numpy.array([[math.cos(pitch), math.sin(pitch), 0.0],
                      [-math.sin(pitch), math.cos(pitch), 0.0],
                      [0.0, 0.0, 1.0]])
    point = numpy.array([x, y, z])
    new = Rx.dot(Ry.dot(Rz.dot(point - center))) + center
    xr, yr, zr = new
    return xr, yr, zr


vrotation = numpy.vectorize(rotation,
                            excluded=['roll', 'yaw', 'pitch', 'center'])
