# Re=200, St=0.8, AR=1.27, psi=90

Simulation of the three-dimensional flow around a pitching and rolling circular flat plate (AR=1.27) at Reynolds number Re=200, Strouhal number St=0.8, with a phase-difference angle of 90 degrees (between the rolling and pitching motions).

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

The simulation computed 10000 time steps in about 9.2 hours on 2 `small-gpu` nodes (20 MPI processes and 2 GPU devices per node) in a Singularity container.

## Post-processing steps

Create a Docker container:

```shell
cd <directory-of-this-README>
docker run --rm -it -v $(pwd):/postprocessing mesnardo/petibm-rollingpitching:prepost /bin/bash
cd /postprocessing  # inside the container
```

and run the instructions displayed in the following sub-sections.

### Compute vorticity components at t/T = 4.25

Compute the vorticity components at time-step index 8500.

* CLI:

  ```shell
  petibm-vorticity -bg 8500 -ed 8500 -step 500
  ```

### Visualize the wake topology

1. Compute the cell-centered streamwise vorticity and Q-criterion at t/T = 4.25

   ```shell
   python scripts/compute_wx_cc.py
   python scripts/compute_qcrit.py
   python scripts/create_qcrit_wx_cc_xdmf.py
   ```

2. Plot the wake topology (side, lateral, and perspective views) at t/T = 4.25 with VisIt

   ```shell
   conda activate py27-visit
   python scripts/visit_plot_qcrit_wx.py
   # Annotate images
   python scripts/process_qcrit_wx_snapshot.py
   conda deactivate
   ```

* Output:
  * `figures/qcrit_wx_perspective_view_0008500.png`
  * `figures/qcrit_wx_lateral_view_0008500.png`
  * `figures/qcrit_wx_top_view_0008500.png`
  * `figures/qcrit_wx_lateral_view_0008500_post.png`
  * `figures/qcrit_wx_top_view_0008500_post.png`

Example: `figures/qcrit_wx_lateral_view_0008500_post.png`

![fig:qcrit_wx_lateral](figures/qcrit_wx_lateral_view_0008500_post.png)

### Compute propulsive performances

* Script: `scripts/get_propulsive_efficiency.py`
* CLI:

  ```shell
  python scripts/get_propulsive_efficiency.py
  ```

* Output:

  ```ascii
  Cycle-averaged thrust: 1.0003222041859
  Cycle-averaged thrust coefficient: 2.553797285085422
  Cycle-averaged hydrodynamic power: 5.868209410178718
  Propulsive efficiency: 0.17046463993782984
  ```
