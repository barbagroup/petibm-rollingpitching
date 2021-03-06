"""Print parameters related to the kinematics of the wing."""

import numpy

import rodney


kinematics = rodney.WingKinematics(AR=2.55, Re=200, St=0.6, nt_period=2000)
print(kinematics)

