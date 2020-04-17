"""Post-process images of Q-criterion."""

import collections
from matplotlib import pyplot
import numpy
import pathlib
import yaml

import rodney


# Parse command line and set directories.
args = rodney.parse_command_line()
simudir = pathlib.Path(__file__).absolute().parents[1]  # simulation directory
figdir = simudir / 'figures'  # directory with figures
annotdir = simudir / 'scripts' / 'annotations'  # config for annotations

# Set default font family and size for Matplotlib figures.
pyplot.rc('font', family='serif', size=16)

# List of time-step indices to process.
timesteps = [7750, 7875, 8000, 8250, 8375, 8500, 8625, 8750, 8875]

for timestep in timesteps:
    print(f'[time-step {timestep}] Annotating snapshot of wake topology ...')

    # Load input image to annotate.
    filepath = figdir / f'qcrit_wx_perspective_zoom_view_{timestep:0>7}.png'
    with open(filepath, 'rb') as infile:
        img = pyplot.imread(infile)

    # Define the size of the Matplotlib figure.
    height, width = img.shape[:2]
    scale = 1 / 100
    figsize = (scale * width, scale * height)

    # Load information about text annotations to add.
    filepath = annotdir / 'qcrit_wx_snapshot_zoom.yaml'
    with open(filepath, 'r') as infile:
        annots = yaml.safe_load(infile)['timesteps']

    # Create Matplotlib figure.
    fig, ax = pyplot.subplots(figsize=figsize)

    # Display input image.
    ax.imshow(img)

    # Scale and set axes limits.
    ax.axis('scaled', adjustable='box')
    ax.axis((0, width, height, 0))
    ax.axis('off')

    # Add arrows to represent direction of the flow.
    filepath = annotdir / f'qcrit_wx_snapshot_zoom_{timestep:0>7}.csv'
    with open(filepath, 'r') as infile:
        arrows = numpy.loadtxt(infile, delimiter=',')
    for i in range(0, len(arrows), 2):
        ax.annotate("", xy=arrows[i + 1], xycoords='data', xytext=arrows[i],
                    arrowprops=dict(facecolor='black', arrowstyle='-|>',
                                    linestyle='-', linewidth=2,
                                    shrinkA=0, shrinkB=0))

    # Add text annotations (with optional arrows) to show vortices.
    if timestep in annots.keys():
        for annot in annots[timestep]:
            if 'xyarrow' in annot.keys():
                ax.annotate(annot['text'], xy=annot['xyarrow'], xycoords='data',
                            xytext=annot['xytext'],
                            arrowprops=dict(facecolor='black', arrowstyle='-|>',
                                            linestyle='--',
                                            shrinkA=0, shrinkB=0))
            else:
                ax.annotate(annot['text'], xy=annot['xytext'], xycoords='data')

    fig.tight_layout()

    if args.save_figures:
        filename = f'qcrit_wx_perspective_zoom_view_{timestep:0>7}_post.png'
        filepath = figdir / filename
        fig.savefig(filepath, dpi=300, bbox_inches='tight')
