#!/usr/bin/env python3
import numpy as np
from decimal import Decimal
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

# Section efficace macroscopique
# de fission thermique
SIGMA_F = 0.09840 

# STEP 1
# résoudre les équations décrivants l'évolution 
# de l'abondance en iode et en xénon

def isotopes_abundance_edo(t, y):
  phi = 3e13

  # apr§s 2 jours
  if (t >= 259200): 
    phi = 0

  # y = [I, X]
  return np.array([
    (GAMMA_I * SIGMA_F * phi) - (LAMBDA_I * y[0]) - (SIGMA_I * y[0] * phi), # edo iode
    (GAMMA_X * SIGMA_F * phi) + (LAMBDA_I * y[0]) - (SIGMA_X * y[1] * phi) - (LAMBDA_X * y[1]) # edo xénon
  ])

def compute_isotopes_abundance(xenon_ci, stop, title):
  # default values
  T0 = 0
  TIME_INTERVAL = 10 # 10s
  STOP = stop
  ISOTOPES_CI = [1.0, xenon_ci] # [I(T_0), X(T_0)]

  title = title
  x_label = "temps (h)"
  y_label = "Abondance"
  legends = ['Iode', 'Xénon']

  isotope_abundance_rk4 = RK4Method(title, y_label, x_label, legends, isotopes_abundance_edo, T0, ISOTOPES_CI, TIME_INTERVAL, STOP)
  isotope_abundance_rk4.resolve()
  isotope_abundance_rk4.graph()

# valeur stables de xénon et iode après 2 jours
def stable_values():
  phi = 3e13

  I = GAMMA_I * SIGMA_F * phi / (LAMBDA_I + SIGMA_I)
  X = (1 / ((SIGMA_X * phi) + LAMBDA_X)) * (GAMMA_X * SIGMA_F * phi) + (LAMBDA_I * I)
  print("Après 2 jours, pour un flux de 3e13 :")
  print('Iode:', '%.2E' % Decimal(I),' Xénon:', '%.2E' % Decimal(X))

# 1. Quantité de xénon initiale : 0.0
# Temps de simulation : 2 jours
stable_values()
compute_isotopes_abundance(xenon_ci=0.0, stop=172800, title="Abondance d'iode et de xénon entre 0 et 2 jours, Xénon au départ : 0")

# 2. Quantité de xénon initiale : 2e15
# Temps de simulation : 5 jours
compute_isotopes_abundance(xenon_ci=2e15, stop=432000, title="Abondance d'iode et de xénon entre 0 et 5 jours, Xénon au départ : 2e15")

# 3. Quantité de xénon initiale : 2e15
# Temps de simulation : 5 jours
# Flux après 3 jours : 0
compute_isotopes_abundance(xenon_ci=2e15, stop=432000, title="Abondance d'iode et de xénon entre 0 et 5 jours, Xénon au départ : 2e15, Flux = 0 après 3 jours")