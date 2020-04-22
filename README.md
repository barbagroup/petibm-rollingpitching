# [Re] Three-dimensional wake topology and propulsive performance of las-aspect-ratio pitching-rolling plates

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://github.com/mesnardo/petibm-rollingpitching/raw/master/LICENSE)
[![Docker Hub](https://img.shields.io/badge/hosted-docker--hub-informational.svg)](https://cloud.docker.com/u/mesnardo/repository/docker/mesnardo/petibm-rollingpitching)
[![Singularity Hub](https://www.singularity-hub.org/static/img/hosted-singularity--hub-%23e32929.svg)](https://singularity-hub.org/collections/2855)

* Olivier Mesnard (The George Washington University)
* Lorena A. Barba (The George Washington University)

This repository contains a computational replication of the scientific findings published by Li and Dong (Physics of Fluids, 2016).

## References

* Li, C., & Dong, H. (2016). Three-dimensional wake topology and propulsive performance of low-aspect-ratio pitching-rolling plates. Physics of Fluids, 28(7), 071901.

## Dependencies

* [PetIBM](https://github.com/barbagroup/PetIBM) (0.5.1)
* [PyDistMesh](https://github.com/bfroehle/pydistmesh) (1.2)
* [PetibmPy](https://github.com/mesnardo/petibmpy) (0.2)
* [VisIt](https://wci.llnl.gov/simulation/computer-codes/visit) (2.12.1)

## Contents

* `rescience-rollingpitching`: manuscript to be submitted to [ReScience C](https://rescience.github.io/)
* `docker`: Dockerfiles used to build Docker images (shared on [DockerHub](https://hub.docker.com/repository/docker/mesnardo/petibm-rollingpitching))
* `singularity`: Singularity recipe files to build images (shared on [Singularity Hub](https://singularity-hub.org/collections/2855))
* `src`: PetIBM application source files for the 3D pitching and rolling plate, and Python pre- and post-processing files.
* `runs`: directory with inputs files of the PetIBM simulations (independence and parametric study)
* `data`: digitized data from Li & Dong (2016) used for comparison with the PetIBM results

## Conda environment for pre- and post-processing

* Install PetibmPy in a conda environment

```shell
cd sfw
wget https://github.com/mesnardo/petibmpy/archive/v0.2.tar.gz
tar -xzf v0.2.tar.gz
cd petibmpy-0.2
conda env create --name=py36-rolling --file=environment.yaml
conda activate py36-rolling
python setup.py install
```

* Install PyDistMesh

```shell
cd sfw
wget https://github.com/bfroehle/pydistmesh/archive/v1.2.tar.gz
tar -xzf v1.2.tar.gz
cd pydistmesh-1.2
conda activate py36-rolling
python setup.py install
```

* Install PETSc (3.12.2) and PetIBM (0.5.1)

To install PETSc, please refer to the [installation instructions](https://www.mcs.anl.gov/petsc/documentation/installation.html).

To install PetIBM, please refer to the [installation instructions](https://barbagroup.github.io/PetIBM/md_doc_markdowns_installation.html).

* Install VisIt (2.12.1)

To install VisIt, please refer to the [installation instructions](https://wci.llnl.gov/simulation/computer-codes/visit/executables).

## LICENSE

**Not all content in this repository is open source.**
The Python code for creating the figures is shared under a BSD 3-Clause License.
The written content in any Jupyter Notebooks is shared under a Creative Commons Attribution (CC-BY) license.
But please note that the manuscript text is not open source; we reserve rights to the article content, which will be submitted for publication in a journal.
Only fair use applies in this case.
