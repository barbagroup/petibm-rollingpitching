#include <petibm/rigidkinematics/rigidkinematics.h>

class RollingPitchingSolver : protected RigidKinematicsSolver
{
public:
    RollingPitchingSolver() = default;

    RollingPitchingSolver(const MPI_Comm &world, const YAML::Node &node);

    ~RollingPitchingSolver();

    using RigidKinematicsSolver::destroy;

    using RigidKinematicsSolver::advance;

    using RigidKinematicsSolver::write;

    using RigidKinematicsSolver::ioInitialData;

    using RigidKinematicsSolver::finished;

    PetscErrorCode init(const MPI_Comm &world, const YAML::Node &node);

protected:
    PetscReal f;
    PetscReal A_phi;
    PetscReal A_theta;
    PetscReal psi;
    PetscReal theta_bias;
    PetscReal c;
    PetscReal Xc;
    PetscReal Yc;
    PetscReal Zc;

    PetscErrorCode setCoordinatesBodies(const PetscReal &ti);
    PetscErrorCode setVelocityBodies(const PetscReal &ti);

}; // RollingPitchingSolver
