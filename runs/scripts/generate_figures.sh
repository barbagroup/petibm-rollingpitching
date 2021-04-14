#!/usr/bin/env bash

cd $(dirname "$(dirname $0)")

conda_dir=/opt/miniconda3
env_name=py36-rolling

. $conda_dir/bin/activate
conda activate $env_name

printf "\n*** Plotting force coefficients (compare Re) ...\n"
python scripts/plot_force_coefficients_compare_Re.py

printf "\n*** Plotting force coefficients (compare AR) ...\n"
python scripts/plot_force_coefficients_compare_AR.py

printf "\n*** Plotting force coefficients (compare psi) ...\n"
python scripts/plot_force_coefficients_compare_psi.py

printf "\n*** Plotting efficiency (compare St) ...\n"
python scripts/plot_efficiency_compare_St.py

printf "\n*** Plotting efficiency (compare psi) ...\n"
python scripts/plot_efficiency_compare_psi.py

exit 0
