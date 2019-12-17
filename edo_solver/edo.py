import numpy as np

from constants import (GAMMA_I, GAMMA_X, SIGMA_F, LAMBDA_I, LAMBDA_X, SIGMA_I, SIGMA_X, 
  PHI, TAU, k, SIGMA_U, SIGMA_B_MAX, SIGMA_B_MIN, SIGMA_B_STEP, STABLE_FLOW, FLOW_START, FLOW_DROP)

def isotopes_abundance_edo (self, t, y):
  # y = [I, X]
  return np.array([
    (GAMMA_I * SIGMA_F * self.phi) - (LAMBDA_I * y[0]) - (SIGMA_I * y[0] * self.phi), # edo iode
    (GAMMA_X * SIGMA_F * self.phi) + (LAMBDA_I * y[0]) - (SIGMA_X * y[1] * self.phi) - (LAMBDA_X * y[1]) # edo xénon
  ])

def neutrons_flow_edo (self, t, y):
  # y = [I, X, PHI]
  return np.array([
    (GAMMA_I * SIGMA_F * y[2]) - (LAMBDA_I * y[0]) - (SIGMA_I * y[0] * y[2]), # edo iode
    (GAMMA_X * SIGMA_F * y[2]) + (LAMBDA_I * y[0]) - (SIGMA_X * y[1] * y[2]) - (LAMBDA_X * y[1]), # edo xénon
    ((y[2] / TAU) * k * (SIGMA_U - (SIGMA_X * y[1]) - self.sigma_b)) # edo flux de neutrons
])