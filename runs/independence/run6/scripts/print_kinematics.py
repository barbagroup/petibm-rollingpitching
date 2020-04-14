"""Print parameters related to the kinematics of the wing."""

import numpy

import rodney


kinematics = rodney.WingKinematics(nt_period=1000)
print(kinematics)

