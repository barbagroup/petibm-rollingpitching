#include "rollingpitching.h"

#include <petibm/io.h>

RollingPitchingSolver::RollingPitchingSolver(const MPI_Comm &world, const YAML::Node & node)
{
    init(world, node);
}  // RollingPitchingSolver::RollingPitchingSolver

RollingPitchingSolver::~RollingPitchingSolver()
{
    PetscErrorCode ierr;
    PetscBool finalized;

    PetscFunctionBeginUser;

    ierr = PetscFinalized(&finalized); CHKERRV(ierr);
    if (finalized) return;

    ierr = destroy(); CHKERRV(ierr);
}  // RollingPitchingSolver::~RollingPitchingSolver

PetscErrorCode RollingPitchingSolver::init(const MPI_Comm &world,
                                    const YAML::Node &node)
{
    PetscErrorCode ierr;

    PetscFunctionBeginUser;

    ierr = RigidKinematicsSolver::init(world, node); CHKERRQ(ierr);

    ierr = PetscLogStagePush(stageInitialize); CHKERRQ(ierr);

    f = 0.0; A_phi = 0.0; A_theta = 0.0; psi = 0.0; theta_bias = 0.0;
    c = 1.0; Xc = 0.0; Yc = 0.0; Zc = 0.0;
    if (node["bodies"][0]["kinematics"])
    {
        const YAML::Node &config_kin = node["bodies"][0]["kinematics"];
        f = config_kin["f"].as<PetscReal>(0.0);
        A_phi = config_kin["A_phi"].as<PetscReal>(0.0);
        A_theta = config_kin["A_theta"].as<PetscReal>(0.0);
        psi = config_kin["psi"].as<PetscReal>(0.0);
        theta_bias = config_kin["theta_bias"].as<PetscReal>(0.0);
        c = node["c"].as<PetscReal>(1.0);
        Xc = config_kin["CoR"][0].as<PetscReal>(0.0);
        Yc = config_kin["CoR"][1].as<PetscReal>(0.0);
        Zc = config_kin["CoR"][2].as<PetscReal>(0.0);
    }

    ierr = setCoordinatesBodies(nstart * dt); CHKERRQ(ierr);

    ierr = PetscLogStagePop(); CHKERRQ(ierr);

    PetscFunctionReturn(0);
}  // RollingPitchingSolver::init

PetscErrorCode RollingPitchingSolver::setCoordinatesBodies(const PetscReal &ti)
{
    PetscReal phi,   /// rolling angle
              theta; /// pitching angle
    petibm::type::SingleBody &body = bodies->bodies[0];
    petibm::type::RealVec2D &coords = body->coords;
    petibm::type::RealVec2D &coords0 = body->coords0;

    PetscFunctionBeginUser;

    phi = -A_phi * PetscCosReal(2 * PETSC_PI * f * ti);
    theta = -A_theta * PetscCosReal(2 * PETSC_PI * f * ti + psi) + theta_bias;

    PetscReal cos_phi = PetscCosReal(phi),
              sin_phi = PetscSinReal(phi),
              cos_theta = PetscCosReal(theta),
              sin_theta = PetscSinReal(theta);

    for (PetscInt k = 0; k < body->nPts; k++)
    {
        coords[k][0] = Xc \
                       + (coords0[k][0] - Xc) * cos_theta \
                       - (coords0[k][1] - Yc) * sin_theta;
        
        coords[k][1] = Yc \
                       + (coords0[k][0] - Xc) * cos_phi * sin_theta \
                       + (coords0[k][1] - Yc) * cos_phi * cos_theta \
                       + (coords0[k][2] - Zc) * sin_phi;
        
        coords[k][2] = Zc \
                       - (coords0[k][0] - Xc) * sin_phi * sin_theta \
                       - (coords0[k][1] - Yc) * sin_phi * cos_theta \
                       + (coords0[k][2] - Zc) * cos_phi;
    }

    PetscFunctionReturn(0);
} // RollingPitchingSolver::setCoordinatesBodies

PetscErrorCode RollingPitchingSolver::setVelocityBodies(const PetscReal &ti)
{
    PetscErrorCode ierr;
    PetscReal **UB_arr;
    petibm::type::SingleBody &body = bodies->bodies[0];
    petibm::type::RealVec2D &coords = body->coords;

    PetscFunctionBeginUser;

    // compute angular velocities
    PetscReal Omega_x, Omega_z;
    Omega_x = 2 * PETSC_PI * f * A_phi * PetscSinReal(2 * PETSC_PI * f * ti);
    Omega_z = 2 * PETSC_PI * f * A_theta * PetscSinReal(2 * PETSC_PI * f * ti + psi);

    // update the boundary velocity array
    ierr = DMDAVecGetArrayDOF(body->da, UB, &UB_arr); CHKERRQ(ierr);
    for (PetscInt k = body->bgPt; k < body->edPt; k++)
    {
        UB_arr[k][0] = - Omega_z * (coords[k][1] - Yc);
        UB_arr[k][1] = Omega_z * (coords[k][0] - Xc) - Omega_x * (coords[k][1] - Yc);
        UB_arr[k][2] = - Omega_x * (coords[k][1] - Yc);
    }
    ierr = DMDAVecRestoreArrayDOF(body->da, UB, &UB_arr); CHKERRQ(ierr);

    PetscFunctionReturn(0);
} // RollingPitchingSolver::setVelocityBodies
