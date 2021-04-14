import os
import shutil
from pathlib import Path

import yaml


scriptdir = Path(__file__).absolute().parent
basedir = scriptdir.parent
outdir = basedir / 'repro-packs'
outdir.mkdir(parents=True, exist_ok=True)

filepath = scriptdir / 'repro-packs.yaml'
with open(filepath, 'r') as infile:
    metadata = yaml.safe_load(infile)

paths = set()
for fig, data in metadata.items():
    parent = Path(fig).parent
    for src in data:
        src = basedir / 'runs' / parent / src
        src = list(Path(src.parent).glob(src.name))
        paths.update(src)

for src in sorted(paths):
    index = src.parts.index('runs')
    src_str = '/'.join(src.parts[index + 1:])
    print(f'Copying {src_str} ...')
    dst = outdir.joinpath(*src.parts[index + 1:])
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)
