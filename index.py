#!/usr/bin/env python3
import numpy as np
from edo_solver.rk4 import RK4Method

# résoudre les équations décrivants l'évolution 
# de l'abondance en iode et en xénon

# constantes de désintégration
LAMBDA_X = 2.0996E-5 # xénon 135
LAMBDA_I = 2.926E-5 # iode 135

# probabilités de production 
# par interaction avec le combustible
GAMMA_X = 0.004  # xénon 135
GAMMA_I = 0.064 # iode 135

# sections efficaces des interactions avec les neutrons
# (probabilité de capture d'un neutron)
SIGMA_X = 2.65E-18 # xénon 135
SIGMA_I = 7E-24 # iode 135

# PHI : Flux de neutrons
PHI = 3e13

# Section efficace macroscopique
# de fission thermique
SIGMA_F = 0.09840 

# default values
T0 = 0
TIME_INTERVAL = 10
STOP = 172800
IODE_CI = [1.0, 0.0]
XENON_CI = [1.0, 0.0]

def iode_abundance(t, I):
  # I[0] = I ; I[1] = I'
  return np.array([
    (GAMMA_I * SIGMA_F * PHI) - (LAMBDA_I * I[0]) - (SIGMA_I * I[0] * PHI)
  ])

iode_abundance_rk4 = RK4Method("Abondance d'iode", "I (iode)", "temps (s)", iode_abundance, T0, IODE_CI, TIME_INTERVAL, STOP)
iode_abundance_rk4.resolve()
iode_abundance_rk4.graph()

def xenon_abundance(t, X):
  I = iode_abundance(t, )
  return np.array([
    (GAMMA_X * SIGMA_F) * (PHI + LAMBDA_I * I[0]) - (SIGMA_X * PHI-LAMBDA_X * X[0])
  ])

xenon_abundance_rk4 = RK4Method("Abondance de xenon", "X (xénon)", "temps (s)", xenon_abundance, T0, XENON_CI, TIME_INTERVAL, STOP)
xenon_abundance_rk4.resolve()
xenon_abundance_rk4.graph()