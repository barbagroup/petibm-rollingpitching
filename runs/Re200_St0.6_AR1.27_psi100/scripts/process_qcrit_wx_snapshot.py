"""Post-process images of Q-criterion to compute inclination angles."""

import collections
import math
from matplotlib import pyplot
import pathlib

import rodney


Point = collections.namedtuple('Point', ['x', 'y'])


class Line(object):
    """Define a line."""

    def __init__(self, point1, point2):
        """Compute slope and intercept given two reference points."""
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

    def create_line_guide(self, point1, point2,
                          extend_left=0.0, extend_right=0.0):
        """Return line guide for Matplotlib figure."""
        x1, x2 = point1.x - extend_left, point2.x + extend_right
        y1, y2 = self.y([x1, x2])
        return (x1, x2), (y1, y2)


# Parse command line and set directories.
args = rodney.parse_command_line()
simudir = pathlib.Path(__file__).absolute().parents[1]
figdir = simudir / 'figures'

# Lateral view: Load PNG image from file.
filepath = figdir / 'qcrit_wx_lateral_view_0000017.png'
with open(filepath, 'rb') as infile:
    img = pyplot.imread(infile)

# Lateral view: Plot the image.
fig, ax = pyplot.subplots(figsize=(12.0, 6.0))
ax.imshow(img)
lims = ax.axis('scaled', adjustable='box')
xstart, xend, yend, ystart = lims
ax.axhline(0.5 * (yend - ystart), xmin=xstart, xmax=xend,
           color='black', linestyle='-.', linewidth=2.0)

# Lateral view: Create inclination line for alpha.
alpha = (Point(263, 215), Point(577, 105))  # in pixels
line = Line(*alpha)
print(f'alpha: {line.get_inclination():.2f}')
ax.plot(*line.create_line_guide(*alpha, extend_left=50, extend_right=250),
        color='black', linestyle='--', linewidth=2.0)

# Lateral view: Set limits and remove axis.
ax.axis((xstart, xend - 100, yend, ystart))
ax.axis('off')
fig.tight_layout()

# Lateral view: Save figure.
if args.save_figures:
    filepath = figdir / 'qcrit_wx_lateral_view_0000017_post.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

# Top view: Load PNG image from file.
filepath = figdir / 'qcrit_wx_top_view_0000017.png'
with open(filepath, 'rb') as infile:
    img = pyplot.imread(infile)

# Top view: Plot the image.
fig, ax = pyplot.subplots(figsize=(12.0, 6.0))
ax.imshow(img)
lims = ax.axis('scaled', adjustable='box')
xstart, xend, yend, ystart = lims
ax.axhline(0.5 * (yend - ystart), xmin=xstart, xmax=xend,
           color='black', linestyle='-.', linewidth=2.0)

# Top view: Compute inclination angle.
gamma = (Point(316, 170), Point(648, 162))  # in pixels
line = Line(*gamma)
print(f'gamma: {line.get_inclination():.2f}')
ax.plot(*line.create_line_guide(*gamma, extend_left=20, extend_right=20),
        color='black', linestyle='--', linewidth=2.0)

# Top view: Set limits and remove axis.
ax.axis((xstart, xend - 100, yend - 50, ystart + 50))
ax.axis('off')
fig.tight_layout()

# Top view: Save figure.
if args.save_figures:
    filepath = figdir / 'qcrit_wx_top_view_0000017_post.png'
    fig.savefig(filepath, dpi=300, bbox_inches='tight')

# Display figures.
if args.show_figures:
    pyplot.show()
