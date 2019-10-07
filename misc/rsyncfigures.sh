#!/usr/bin/env bash
# Rsync all figures.

scriptdir="$( cd "$(dirname "$0")" ; pwd -P )"
rootdir="$( cd "$(dirname "$scriptdir")" ; pwd -P )"
outdir="$rootdir/allfigures"

python $scriptdir/listfigures.py

listpath="$scriptdir/listfigures.txt"
mkdir -p $outdir

rsync -av --files-from=$listpath --delete $rootdir $outdir

rm -f $listpath

exit 0
