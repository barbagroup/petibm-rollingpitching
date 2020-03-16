"""Functions to generate plots of the flow field with VisIt."""

import os
import sys
import yaml


VISIT_DIR = os.environ.get('VISIT_DIR', 'fake')
VISIT_ARCH = os.environ.get('VISIT_ARCH', 'fake')
pkgs_dir = os.path.join(VISIT_DIR, VISIT_ARCH, 'lib', 'site-packages')
if not os.path.exists(pkgs_dir):
    raise ValueError('Set env variables VISIT_DIR and VISIT_ARCH')
sys.path.append(pkgs_dir)
import visit

VISIT_MAKEMOVIE = os.path.join(VISIT_DIR, VISIT_ARCH, 'bin', 'makemovie.py')


def visit_initialize():
    """Launch VisIt in no-window mode and check VisIt version."""
    visit.LaunchNowin()
    visit_check_version()


def visit_finalize():
    """Terminate engine and close VisIt."""
    os.remove('visitlog.py')  # remove VisIt-generated log file
    visit.CloseComputeEngine()
    visit.Close()


def visit_check_version():
    """Check the version of VisIt being used."""
    version = visit.Version()  # current version
    script_version = '2.12.1'  # version used to create this script

    if version != script_version:
        print('[warning] You are using VisIt-{}.'.format(version))
        print('[warning] This script was created with VisIt-{}.'
              .format(script_version))
        print('[warning] It may not work as expected')


def visit_get_view(filepath, dim):
    """Create a VisIt view.

    Parameters
    ----------
    filepath : str
        Path of the YAML file with the view configuration.
    dim : int
        Number of dimensions of the application (either 2 or 3).

    Returns
    -------
    visit.View2DAttributes or visit.View3DAttributes
        The view attributes.

    """
    # Check number of dimensions is 2 or 3.
    assert dim in [2, 3], 'Incorrect dimension (use dim=2 or dim=3)'

    # Load YAML node from file.
    node = 'View{}DAtts'.format(dim)
    with open(filepath, 'r') as infile:
        config = yaml.load(infile)[node]

    # Set attributes of the view.
    ViewAtts = getattr(visit, 'View{}DAttributes'.format(dim))()
    for key, value in config.items():
        if type(value) is list:
            value = tuple(value)
        setattr(ViewAtts, key, value)

    return ViewAtts


def visit_get_states(state=None, states=None, states_range=[0, None, 1]):
    """Get the state indices to render.

    state : int, optional
        Single state index to render;
        default is None (i.e., render multiple states).
    states : list, optional
        List of states to render; default is None (i.e., render all states).
    states_range : list, optional
        Start, end, and step indices for states to render;
        default is [0, None, 1] (i.e., render all states).

    Returns
    -------
    list
        List of state indices to render.

    """
    if state is not None:
        states = [state]
    elif states is None:
        if states_range[1] is None:
            states_range[1] = visit.TimeSliderGetNStates()
        else:
            states_range[1] += 1
        states = list(range(*states_range))
    return states


def visit_render_save_states(states,
                             config_view=None,
                             out_dir=os.getcwd(),
                             prefix=None,
                             figsize=(1024, 1024)):
    """Render and save states into PNG files.

    Parameters
    ----------
    states : list-alike
        List of states to render and save.
    config_view : str, optional
        Path of the YAML file with the configuration of the view;
        default is None (use default VisIt view).
    out_dir : str, optional
        Output directory; created is non-existent;
        default is the present working directory (".").
    prefix : str, optional
        Filename prefix; default is "None" (no prefix).
    figsize : tuple
        Figure width and height (in pixels); default is (1024, 1024).

    """
    visit.Source(VISIT_MAKEMOVIE)
    visit.ToggleCameraViewMode()

    # Create output directory if necessary.
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    # Define common attributes to save the window.
    SaveWindowAtts = visit.SaveWindowAttributes()
    SaveWindowAtts.outputToCurrentDirectory = 0
    SaveWindowAtts.outputDirectory = out_dir
    SaveWindowAtts.family = 0
    SaveWindowAtts.format = SaveWindowAtts.PNG
    SaveWindowAtts.width, SaveWindowAtts.height = figsize
    SaveWindowAtts.quality = 100
    SaveWindowAtts.resConstraint = SaveWindowAtts.NoConstraint

    # Define common rendering attributes.
    RenderingAtts = visit.RenderingAttributes()

    # Parse YAML file with the 3D view configuration.
    if config_view is not None:
        View3DAtts = visit_get_view(config_view, 3)

    # Loop over the states to render and save the plots.
    for i, state in enumerate(states):
        print('[state {}] Rendering and saving figure ...'.format(state))
        visit.SetTimeSliderState(state)

        if i == 0:
            visit.DrawPlots()
            visit.SetView3D(View3DAtts)

        # Set rendering attributes.
        visit.SetRenderingAttributes(RenderingAtts)

        # Set state-specific attributes to save the window.
        SaveWindowAtts.fileName = '{}{:0>7}'.format(prefix, state)
        visit.SetSaveWindowAttributes(SaveWindowAtts)

        visit.SaveWindow()


def visit_plot_qcrit_wx_3d(xdmf_path,
                           qcrit_vals=(6.0, 1.0),
                           wx_lims=(-5.0, 5.0),
                           config_view=None,
                           out_dir=os.getcwd(),
                           prefix='qcrit_wx_3d_',
                           figsize=(1024, 1024),
                           state=None, states=None,
                           states_range=[0, None, 1]):
    """Plot the 3D isosurface of the Q-criterion at 2 values.

    The first isosurface is colored by the streamwise vorticity.
    The second isosurface is colored with a single color (grey).

    Parameters
    ----------
    xdmf_path : str
        Path of the XDMF file with information about the Q-criterion and
        the streamwise vorticity.
    qcrit_vals : tuple, optional
        Values of the Q-criterion to display as a tuple of 2 floats;
        default is (6.0, 1.0).
    wx_lims : tuple, optional
        Limits of the color range for the streamwise vorticity
        as a tuple of 2 floats; default is (-5.0, 5.0).
    config_view : str, optional
        Path of the YAML file with the configuration of the view;
        default is None (use default VisIt view).
    out_dir : str, optional
        Output directory in which figures will be saved;
        default is the present working directory.
    prefix : str, optional
        Output filename prefix; default is "qcrit_wx_3d_".
    figsize : tuple
        Figure width and height (in pixels); default is (1024, 1024).
    state : int, optional
        Single state index to render;
        default is None (i.e., render multiple states).
    states : list, optional
        List of states to render; default is None (i.e., render all states).
    states_range : list, optional
        Start, end, and step indices for states to render;
        default is [0, None, 1] (i.e., render all states).

    """
    visit_initialize()

    # Open database from XDMF file.
    visit.OpenDatabase(xdmf_path, 0)

    # Add a pseudocolor of the streamwise vorticity.
    visit.AddPlot('Pseudocolor', 'wx_cc', 1, 0)
    PseudocolorAtts = visit.PseudocolorAttributes()
    PseudocolorAtts.minFlag, PseudocolorAtts.maxFlag = 1, 1
    PseudocolorAtts.min, PseudocolorAtts.max = wx_lims
    PseudocolorAtts.colorTableName = 'viridis'
    PseudocolorAtts.invertColorTable = 0
    visit.SetPlotOptions(PseudocolorAtts)

    # Add isosurface of the Q-criterion (colored by streamwise vorticity).
    visit.AddOperator('Isosurface', 0)
    IsosurfaceAtts = visit.IsosurfaceAttributes()
    IsosurfaceAtts.contourMethod = IsosurfaceAtts.Value
    IsosurfaceAtts.contourValue = (qcrit_vals[0])
    IsosurfaceAtts.variable = 'qcrit'
    visit.SetOperatorOptions(IsosurfaceAtts, 0)

    # Add single-value contour of the Q-criterion.
    visit.AddPlot('Contour', 'qcrit', 1, 0)
    ContourAtts = visit.ContourAttributes()
    ContourAtts.colorType = ContourAtts.ColorBySingleColor
    ContourAtts.legendFlag = 0
    ContourAtts.singleColor = (128, 128, 128, 153)  # grey
    ContourAtts.contourNLevels = 1
    ContourAtts.minFlag, ContourAtts.maxFlag = 1, 1
    ContourAtts.min, ContourAtts.max = qcrit_vals[1], qcrit_vals[1]
    visit.SetPlotOptions(ContourAtts)

    # Remove some annotations; keep triad.
    AnnotationAtts = visit.AnnotationAttributes()
    AnnotationAtts.userInfoFlag = 0
    AnnotationAtts.databaseInfoFlag = 0
    AnnotationAtts.timeInfoFlag = 0
    AnnotationAtts.legendInfoFlag = 0
    AnnotationAtts.axes3D.visible = 0
    AnnotationAtts.axes3D.triadFlag = 1
    AnnotationAtts.axes3D.bboxFlag = 0
    visit.SetAnnotationAttributes(AnnotationAtts)

    # Define state indices to render.
    states = visit_get_states(state=state, states=states,
                              states_range=states_range)

    # Render states and save figures to files.
    visit_render_save_states(states,
                             config_view=config_view,
                             out_dir=out_dir, prefix=prefix,
                             figsize=figsize)

    visit_finalize()
