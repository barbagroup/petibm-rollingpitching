"""Print parameters related to the kinematics of the wing."""

import numpy

import rodney


kinematics = rodney.WingKinematics(Re=200, St=1.0, nt_period=2000)
print(kinematics)

