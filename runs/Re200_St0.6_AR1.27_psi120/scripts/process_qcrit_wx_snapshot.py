"""Post-process images of Q-criterion to compute inclination angles."""

import collections
import math
from matplotlib import patches, pyplot
import pathlib

import rodney


Point = collections.namedtuple('Point', ['x', 'y'])


def get_midpoint(point1, point2):
    """Return the midpoint."""
    return Point(0.5 * (point1.x + point2.x),
                 0.5 * (point1.y + point2.y))


class Line(object):
    """Define a line."""

    def __init__(self, point1, point2):
        """Compute slope and intercept given two reference points."""
        self.p1, self.p2 = point1, point2
        self.a, self.b = self._slope_intercept(point1, point2)

    def _slope_intercept(self, point1, point2):
        """Compute and return slope and intercept."""
        a = (point2.y - point1.y) / (point2.x - point1.x)
        b = point1.y - a * point1.x
        return a, b

    def y(self, x):
        """Compute y given x."""
        if hasattr(x, "__iter__"):
            return (self.a * xi + self.b for xi in x)
        return self.a * x + self.b

    def get_inclination(self, degrees=True):
        """Compute adn return inclination angle w.r.t. horizontal axis."""
        x1, x2 = 0.0, 1.0
        y1, y2 = self.y([x1, x2])
        length = math.sqrt((y2 - y1)**2 + (x2 - x1)**2)
        alpha = math.acos(abs(x2 - x1) / length)
        if degrees:
            alpha *= 180.0 / math.pi
        return alpha

    def extend(self, left=0.0, right=0.0):
        """Return a new extended line."""
        x1, x2 = self.p1.x - left, self.p2.x + right
        y1, y2 = self.y([x1, x2])
        return Line(Point(x1, y1), Point(x2, y2))

    def limits(self):
        """Return line limits as tuples."""
        return (self.p1.x, self.p2.x), (self.p1.y, self.p2.y)


def annotate_angle(ax, text, xloc, line, hline, buf=50):
    """Annotate angle between two given lines."""
    posA, posB = Point(xloc, line.y(xloc)), Point(xloc, hline.y(xloc))
    arrowstyle = '<->,head_length=5,head_width=3'
    arrow = patches.FancyArrowPatch(posA=(posA.x, posA.y),
                                    posB=(posB.x, posB.y),
                                    arrowstyle=arrowstyle,
                                    color='black', linewidth=2.0,
                                    connectionstyle='arc3,rad=-0.5')
    ax.add_patch(arrow)
    ax.annotate(text, xy=(xloc + buf, get_midpoint(posA, posB).y))


# Parse command line and set directories.
args = rodney.parse_command_line()
simudir = pathlib.Path(__file__).absolute().parents[1]
figdir = simudir / 'figures'

# Set default font family and size for Matplotlib figures.
pyplot.rc('font', family='serif', size=16)

# --------------------------------------------------------------
# Post-process lateral view: compute and add inclination angles.
# --------------------------------------------------------------

# Load PNG image from file.
filepath = figdir / 'qcrit_wx_lateral_view_0008500.png'
with open(filepath, 'rb') as infile:
    img = pyplot.imread(infile)

# Plot the image.
fig, ax = pyplot.subplots(figsize=(6.0, 4.0))
ax.imshow(img)
xstart, xend, yend, ystart = ax.axis('scaled', adjustable='box')
ymid = 0.5 * (yend - ystart)

# Compute and plot inclination line for alpha.
ring1 = get_midpoint(Point(233, 154), Point(341, 209))  # first vortex ring
ring2 = get_midpoint(Point(400, 75), Point(509, 141))  # second vortex ring
alpha = Line(ring1, ring2)  # line passing through the vortex ring centers
print(f'alpha: {alpha.get_inclination():.2f}')
line = alpha.extend(left=100, right=200)
ax.plot(*line.limits(), color='black', linestyle='--', linewidth=3.0)
hline = Line(Point(xstart, ymid), Point(xend, ymid))
ax.plot(*hline.limits(), color='black', linestyle='-.', linewidth=3.0)
annotate_angle(ax, r'$\alpha$', 520, line, hline, buf=75)

# Set limits and remove axes.
ax.axis((xstart, xend - 100, yend, ystart))
ax.axis('off')
fig.tight_layout()

# Save figure.
if args.save_figures:
    filepath = figdir / 'qcrit_wx_lateral_view_0008500_post.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

# ----------------------
# Post-process top view.
# ----------------------

# Load PNG image from file.
filepath = figdir / 'qcrit_wx_top_view_0008500.png'
with open(filepath, 'rb') as infile:
    img = pyplot.imread(infile)

# Plot the image.
fig, ax = pyplot.subplots(figsize=(6.0, 4.0))
ax.imshow(img)
xstart, xend, yend, ystart = ax.axis('scaled', adjustable='box')
ymid = 0.5 * (ystart + yend)
ax.axhline(0.5 * (yend - ystart), xmin=xstart, xmax=xend,
           color='black', linestyle='-.', linewidth=3.0)

# Compute inclination angle gamma.
ring1 = get_midpoint(Point(267, 119), Point(288, 252))  # first vortex ring
ring2 = get_midpoint(Point(427, 95), Point(452, 240))  # second vortex ring
gamma = Line(ring1, ring2)  # line passing through the vortex ring centers
print(f'gamma: {gamma.get_inclination():.2f}')
line = gamma.extend(left=100, right=200)
ax.plot(*line.limits(), color='black', linestyle='--', linewidth=3.0)
hline = Line(Point(xstart, ymid), Point(xend, ymid))
annotate_angle(ax, '', 600, line, hline)
ax.annotate(r'$\gamma$', xy=(600, 250))

# Set limits and remove axis.
ax.axis((xstart, xend - 100, yend - 50, ystart + 50))
ax.axis('off')
fig.tight_layout()

# Save figure.
if args.save_figures:
    filepath = figdir / 'qcrit_wx_top_view_0008500_post.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

# Display figures.
if args.show_figures:
    pyplot.show()
