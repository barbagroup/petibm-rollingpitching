#!/usr/bin/env bash

cd $(dirname "$(dirname $0)")

conda_dir=/opt/miniconda3
env_name=py36-rolling
visit_env_name=py27-visit

. $conda_dir/bin/activate
conda activate $env_name

printf "\n*** Generating the vorticity fields ...\n"
petibm-vorticity -bg 8500 -ed 8500 -step 500

printf "\n*** Computing the Q-criterion ...\n"
python scripts/compute_qcrit.py

printf "\n*** Computing the cell-centered streamwise voriticty ...\n"
python scripts/compute_wx_cc.py

printf "\n*** Generating XDMF file for VisIt ...\n"
python scripts/create_qcrit_wx_cc_xdmf.py

printf "\n*** Plotting with VisIt ...\n"
conda activate $visit_env_name
python scripts/visit_plot_qcrit_wx_zoom.py
conda deactivate

printf "\n*** Annotating figures ...\n"
python scripts/process_qcrit_wx_snapshot_zoom.py

printf "\n*** Plotting vorticity slices ...\n"
python scripts/plot_vorticity_slices.py

exit 0
