#!/usr/bin/env python3
import numpy as np
from edo_solver.rk4 import RK4Method

# CONSTANTES #

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

# STEP 1
# résoudre les équations décrivants l'évolution 
# de l'abondance en iode et en xénon

def isotopes_abundance_edo(t, y):
  # y = [I, X]
  return np.array([
    (GAMMA_I * SIGMA_F * PHI) - (LAMBDA_I * y[0]) - (SIGMA_I * y[0] * PHI), # edo iode
    (GAMMA_X * SIGMA_F) * (PHI + LAMBDA_I * y[0]) - (SIGMA_X * PHI-LAMBDA_X * y[1]) # edo xénon
  ])

def compute_isotopes_abundance():
  # default values
  T0 = 0
  TIME_INTERVAL = 10 # 10s
  STOP = 172800 # 2 jours
  ISOTOPES_CI = [1.0, 1.0] # [I(T_0), X(T_0)]

  title = "Abondance d'iode et de xénon entre 0 et 48h"
  x_label = "temps (h)"
  y_label = "Abondance"
  legends = ['Iode', 'Xénon']

  isotope_abundance_rk4 = RK4Method(title, y_label, x_label, legends, isotopes_abundance_edo, T0, ISOTOPES_CI, TIME_INTERVAL, STOP)
  isotope_abundance_rk4.resolve()
  isotope_abundance_rk4.graph()

compute_isotopes_abundance()