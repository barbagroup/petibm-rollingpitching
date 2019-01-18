#include <petscsys.h>
#include <yaml-cpp/yaml.h>

#include <petibm/parser.h>

#include "rollingpitching.h"

int main(int argc, char **argv)
{
    PetscErrorCode ierr;
    YAML::Node config;
    RollingPitchingSolver solver;

    ierr = PetscInitialize(&argc, &argv, nullptr, nullptr); CHKERRQ(ierr);
    ierr = PetscLogDefaultBegin(); CHKERRQ(ierr);

    // parse configuration files; store info in YAML node
    ierr = petibm::parser::getSettings(config); CHKERRQ(ierr);

    // initialize the decoupled IBPM solver
    ierr = solver.init(PETSC_COMM_WORLD, config); CHKERRQ(ierr);
    ierr = solver.ioInitialData(); CHKERRQ(ierr);
    ierr = PetscPrintf(PETSC_COMM_WORLD,
                       "Completed initialization stage\n"); CHKERRQ(ierr);

    // integrate the solution in time
    while (!solver.finished())
    {
        // compute the solution at the next time step
        ierr = solver.advance(); CHKERRQ(ierr);
        // output data to files
        ierr = solver.write(); CHKERRQ(ierr);
    }

    // destroy the decoupled IBPM solver
    ierr = solver.destroy(); CHKERRQ(ierr);

    ierr = PetscFinalize(); CHKERRQ(ierr);

    return 0;
}  // main
