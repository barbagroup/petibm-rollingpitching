#!/usr/bin/env bash

cd $(dirname "$(dirname $0)")

printf "\n*** Generating figures (independence study) ...\n"
/bin/bash independence/scripts/generate_figures.sh

printf "\n*** Generating figures (baseline case) ...\n"
/bin/bash Re200_St0.6_AR1.27_psi90/scripts/generate_figures.sh

printf "\n*** Generating figures (St=0.4) ...\n"
/bin/bash Re200_St0.4_AR1.27_psi90/scripts/generate_figures.sh

printf "\n*** Generating figures (St=0.8) ...\n"
/bin/bash Re200_St0.8_AR1.27_psi90/scripts/generate_figures.sh

printf "\n*** Generating figures (Re=100) ...\n"
/bin/bash Re100_St0.6_AR1.27_psi90/scripts/generate_figures.sh

printf "\n*** Generating figures (Re=400) ...\n"
/bin/bash Re400_St0.6_AR1.27_psi90/scripts/generate_figures.sh

printf "\n*** Generating figures (AR=1.91) ...\n"
/bin/bash Re200_St0.6_AR1.91_psi90/scripts/generate_figures.sh

printf "\n*** Generating figures (AR=2.55) ...\n"
/bin/bash Re200_St0.6_AR2.55_psi90/scripts/generate_figures.sh

printf "\n*** Generating figures (psi=100) ...\n"
/bin/bash Re200_St0.6_AR1.27_psi100/scripts/generate_figures.sh

printf "\n*** Generating figures (psi=110) ...\n"
/bin/bash Re200_St0.6_AR1.27_psi110/scripts/generate_figures.sh

printf "\n*** Generating figures (psi=120) ...\n"
/bin/bash Re200_St0.6_AR1.27_psi120/scripts/generate_figures.sh

printf "\n*** Generating all other figures ...\n"
/bin/bash scripts/generate_figures.sh

exit 0
