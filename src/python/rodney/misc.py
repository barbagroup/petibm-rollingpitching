"""Miscellaneous helper functions."""

import argparse


def parse_command_line():
    """Parse the command-line options."""
    formatter_class = argparse.ArgumentDefaultsHelpFormatter
    descr = 'Generic command-line parser for the rolling-piching application.'
    parser = argparse.ArgumentParser(description=descr,
                                     formatter_class=formatter_class)
    parser.add_argument('--no-show', dest='show_figures',
                        action='store_false',
                        help='Do not display Matplotlib figures')
    parser.add_argument('--no-save', dest='save_figures',
                        action='store_false',
                        help='Do not save Matplotlib figures')
    parser.add_argument('--no-data', dest='extra_data',
                        action='store_false',
                        help='Add extra data for comparison (if available)')
    return parser.parse_args()
