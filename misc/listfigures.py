"""Build the list of figure files to rsync."""

import pathlib


scriptdir = pathlib.Path(__file__).absolute().parent
rootdir = scriptdir.parent
runsdir = rootdir / 'runs'

key = 'figures'  # string to search for in paths
suffixes = ['.png', '.pdf']  # extensions of files to rsync

filepath = scriptdir / 'listfigures.txt'  # path of the output
with open(filepath, 'w') as outfile:
    filepaths = [p for p in runsdir.rglob('*')
                 if not p.is_dir() and
                 key in p.as_posix() and
                 p.suffix in suffixes]
    outfile.writelines([str(p.relative_to(rootdir)) + '\n' for p in filepaths])
