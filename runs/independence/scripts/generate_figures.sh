#!/usr/bin/env bash

cd $(dirname "$(dirname $0)")

conda_dir=/opt/miniconda3
env_name=py36-rolling

. $conda_dir/bin/activate
conda activate $env_name

printf "\n*** Plotting force coefficients (compare dx) ...\n"
python scripts/plot_force_coefficients_compare_dx.py

printf "\n*** Plotting force coefficients (compare disk) ...\n"
python scripts/plot_force_coefficients_compare_disk.py

printf "\n*** Plotting force coefficients (compare dt) ...\n"
python scripts/plot_force_coefficients_compare_dt.py

printf "\n*** Plotting velocity profiles ...\n"
python scripts/plot_velocity_profiles_compare_dx_dt.py

printf "\n*** Plotting kinetic energy profiles ...\n"
python scripts/plot_kinetic_profiles_compare_dx_dt.py

printf "\n*** Generating vorticity fields at t/T=4.25 ...\n"
petibm-vorticity -directory run3 -bg 8500 -ed 8500 -step 500
petibm-vorticity -directory run4 -bg 8500 -ed 8500 -step 500
petibm-vorticity -directory run6 -bg 4250 -ed 4250 -step 250

printf "\n*** Plotting streamwise vorticity slices ...\n"
python scripts/get_wx_distances.py

exit 0
