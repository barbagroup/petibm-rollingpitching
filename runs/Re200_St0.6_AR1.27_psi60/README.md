# Re=200, St=0.6, AR=1.27, psi=60

Simulation of the three-dimensional flow around a pitching and rolling circular flat plate (AR=1.27) at Reynolds number Re=200, Strouhal number St=0.6, with a phase-difference angle of 60 degrees (between the rolling and pitching motions).

## Contents

* `config`: folder with configuration files for the iterative solvers (with PETSc and AmgX).
* `config.yaml`: PetIBM simulation configuration file.
* `probes.yaml`: PetIBM configuration file for volume probes (to monitor the solution in sub-domain of the computational box).
* `scripts`: Python pre- and post-processing scripts.
* `pegasus.slurm`: SLURM script to submit the job on Pegasus (GWU HPC cluster).
* `figures`: folder with post-processing figures.

## Pre-processing steps

Create a Docker container:

```shell
cd <directory-of-this-README>
docker run --rm -it -v $(pwd):/postprocessing mesnardo/petibm-rollingpitching:prepost /bin/bash
cd /postprocessing  # inside the container
```

and run the instructions displayed in the following sub-sections.

### Create the body file for the wing

* Script: `scripts/create_body.py`
* Output: `wing.body`
* CLI:

  ```shell
  python scripts/create_body.py
  ```

## Submit the simulation job

The simulation job was submitted to SLURM scheduling system on Pegasus (HPC cluster at GWU), requesting 2 nodes of the `small-gpu` partition; CLI: `sbatch pegasus.slurm`.
(Note: The SLURM submission script was designed for the user `mesnardo` to run on Pegasus; do not use it as such; use it as an example to develop your own submission script.)

Hardware configuration of small GPU nodes:

* Dell PowerEdge R740 server
* (2) NVIDIA Tesla V100 GPU
* Dual 20-Core 3.70GHz Intel Xeon Gold 6148 processors
* 192GB of 2666MHz DDR4 ECC Register DRAM
* 800 GB SSD onboard storage (used for boot and local scratch space)
* Mellanox EDR Infiniband controller to 100GB fabric

The simulation computed 10000 time steps in about 8.1 hours on 2 `small-gpu` nodes (20 MPI processes and 2 GPU devices per node) in a Singularity container.

## Post-processing steps

Create a Docker container:

```shell
cd <directory-of-this-README>
docker run --rm -it -v $(pwd):/postprocessing mesnardo/petibm-rollingpitching:prepost /bin/bash
cd /postprocessing  # inside the container
```

and run the instructions displayed in the following sub-sections.

### Compute propulsive performances

* Script: `scripts/get_propulsive_efficiency.py`
* CLI:

  ```shell
  python scripts/get_propulsive_efficiency.py
  ```

* Output:

  ```ascii
  Cycle-averaged thrust: 0.08281561673890445
  Cycle-averaged thrust coefficient: 0.2114261747919622
  Cycle-averaged hydrodynamic power: 2.795667557257885
  Propulsive efficiency: 0.029622841429734828
  ```
