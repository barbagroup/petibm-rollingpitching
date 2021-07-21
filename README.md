# [Re] Three-dimensional wake topology and propulsive performance of low-aspect-ratio pitching-rolling plates

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://github.com/mesnardo/petibm-rollingpitching/raw/master/LICENSE)
[![Docker Hub](https://img.shields.io/badge/hosted-docker--hub-informational.svg)](https://cloud.docker.com/u/mesnardo/repository/docker/mesnardo/petibm-rollingpitching)
[![Singularity Hub](https://www.singularity-hub.org/static/img/hosted-singularity--hub-%23e32929.svg)](https://singularity-hub.org/collections/2855)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4733323.svg)](https://doi.org/10.5281/zenodo.4733323)

* Olivier Mesnard (The George Washington University)
* Lorena A. Barba (The George Washington University)

This repository contains a computational replication of the scientific findings published by Li and Dong (Physics of Fluids, 2016).

## References

* Li, C., & Dong, H. (2016). Three-dimensional wake topology and propulsive performance of low-aspect-ratio pitching-rolling plates. Physics of Fluids, 28(7), 071901.

## Contents

* `rescience-rollingpitching`: manuscript to be submitted to [ReScience C](https://rescience.github.io/)
* `docker`: Dockerfiles used to build Docker images (shared on [DockerHub](https://hub.docker.com/repository/docker/mesnardo/petibm-rollingpitching))
* `singularity`: Singularity recipe files to build images (shared on [Singularity Hub](https://singularity-hub.org/collections/2855))
* `src`: PetIBM application source files for the 3D pitching and rolling plate, and Python data-processing package
* `runs`: directory with inputs files of the PetIBM simulations (independence and parametric study)

## Dependencies

* [PetIBM](https://github.com/barbagroup/PetIBM) (0.5.1)
* [PETSc](https://www.mcs.anl.gov/petsc/download/index.html) (3.12.2)
* [PyDistMesh](https://github.com/bfroehle/pydistmesh) (1.2)
* [PetibmPy](https://github.com/mesnardo/petibmpy) (0.2)
* [VisIt](https://wci.llnl.gov/simulation/computer-codes/visit) (2.12.3)

## Container images

* Olivier Mesnard & Lorena A. Barba (2021). [Re] Three-dimensional wake topology and propulsive performance of low-aspect-ratio pitching-rolling plates (container images). [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5090342.svg)](https://doi.org/10.5281/zenodo.5090342)

The deposit (4.7GB) contains the Docker and Singularity images used for the replication:

* `petibm-rollingpitching_PetIBM0.5.1-xenial.tar`: tar archive of the Docker image `mesnardo/petibm-rollingpitching:PetIBM0.5.1-xenial` which includes the PetIBM application for the 3D rolling and pitching wing
* `petibm-rollingpitching_PetIBM0.5.1-xenial.sif`: Singularity image (build from the Docker image) that was used to run the simulations on the `pegasus` HPC cluster (at the George Washington University)
* `petibm-rollingpitching_prepost.tar`: tar archive of the Docker image `mesnardo/petibm-rollingpitching:prepost` which contains all tools to pre- and post-process the numerical outputs of the simulations

We used Docker 1.39 (see [version info](docker/Docker.version)) and Singularity 3.4.2.

## Hardware configuration and run times

See [this README section](runs/README.md/#hardware-configuration-and-run-times).

## Reproducibility packages

* Olivier Mesnard & Lorena A. Barba (2021). [Re] Three-dimensional wake topology and propulsive performance of low-aspect-ratio pitching-rolling plates (repro-packs). [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4732946.svg)](https://doi.org/10.5281/zenodo.4732946)

Download the Zenodo archive (18.6 GB) with the primary data output from PetIBM.

| :warning: WARNING |
|:-|
| Generating secondary data (e.g., 3D vorticity field) requires a machine with more than 16 GB of memory (32 GB is recommended). If you do not have access to such machine, one solution is to launch a `t3.2xlarge` EC2 instance on AWS and run the Docker container there (see [instructions](misc/repro-packs-on-aws.md)). |

Generate all secondary data and figures of the manuscript (~20 minutes):

```shell
cd repro-packs
docker run --rm -it -v $(pwd):/postprocessing mesnardo/petibm-rollingpitching:prepost /bin/bash /postprocessing/scripts/generate_all_figures.sh > repro-packs.log 2>&1
```

## LICENSE

**Not all content in this repository is open source.**
The PetIBM application code and Python scripts are shared under a BSD 3-Clause License.
But please note that the manuscript text is not open source; we reserve rights to the article content, which will be submitted for publication in a journal.
Only fair use applies in this case.
