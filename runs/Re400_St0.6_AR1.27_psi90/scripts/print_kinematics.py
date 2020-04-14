"""Print parameters related to the kinematics of the wing."""

import numpy

import rodney


kinematics = rodney.WingKinematics(Re=400, St=0.6, nt_period=2000)
print(kinematics)

