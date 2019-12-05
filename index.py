#!/usr/bin/env python3
import numpy as np
from decimal import Decimal
from edo_solver.rk4 import RK4Method
from edo_solver.neutrons_flow import NeutronsFlow
from PyInquirer import prompt, print_json

from utils import day_to_seconds
from constants import GAMMA_I, GAMMA_X, SIGMA_F, LAMBDA_I, LAMBDA_X, SIGMA_I, SIGMA_X, PHI, TAU, k, SIGMA_U, SIGMA_B_MAX, SIGMA_B_MIN, SIGMA_B_STEP, STABLE_FLOW

def isotopes_abundance_edo (self, t, y):
  # après 3 jours
  if (self._modify_flow and t >= day_to_seconds(self._day_of_modification)): 
    self._phi = self._next_flow

  # y = [I, X]
  return np.array([
    (GAMMA_I * SIGMA_F * self._phi) - (LAMBDA_I * y[0]) - (SIGMA_I * y[0] * self._phi), # edo iode
    (GAMMA_X * SIGMA_F * self._phi) + (LAMBDA_I * y[0]) - (SIGMA_X * y[1] * self._phi) - (LAMBDA_X * y[1]) # edo xénon
  ])

def compute_isotopes_abundance (xenon_ci, stop, title, modify_flow = False, day_of_modification = None, next_flow = None):
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
def stable_values ():
  phi = PHI

  I = (GAMMA_I * SIGMA_F * phi) / (LAMBDA_I + SIGMA_I * phi)
  X = ((GAMMA_X * SIGMA_F * phi) + (LAMBDA_I * I)) / ((SIGMA_X * phi) + (LAMBDA_X))
  #X = (1 / ((SIGMA_X * phi) + LAMBDA_X)) * (GAMMA_X * SIGMA_F * phi) + (LAMBDA_I * I)
  print("Après 2 jours, pour un flux de 3e13 :")
  print('Iode:', '%.2E' % Decimal(I),' Xénon:', '%.2E' % Decimal(X))

def neutrons_flow_edo (self, t, y, modify_flow, day_of_modification, next_flow):
  print('Flux de neutrons:', '%.2E' % Decimal(y[2]))

  # Si le flux est plus bas que le flux stable
  # et que sigma_b ne descend pas en dessous de la valeur minimale
  # on diminue la section efficace des neutrons (sigma_b)
  #print(y[2])
  if (y[2] < STABLE_FLOW and self._sigma_b > SIGMA_B_MIN):
    self._sigma_b -= SIGMA_B_STEP
  
  # Si le flux est plus haut que le flux stable 
  # et que sigma_b ne dépasse pas sa valeur maximale
  # on diminue la section efficace des neutrons (sigma_b)
  elif (y[2] > STABLE_FLOW and self._sigma_b < SIGMA_B_MAX):
    self._sigma_b += SIGMA_B_STEP
  
  # y = [I, X, PHI]
  return np.array([
    (GAMMA_I * SIGMA_F * y[2]) - (LAMBDA_I * y[0]) - (SIGMA_I * y[0] * y[2]), # edo iode
    (GAMMA_X * SIGMA_F * y[2]) + (LAMBDA_I * y[0]) - (SIGMA_X * y[1] * y[2]) - (LAMBDA_X * y[1]), # edo xénon
    ((y[2] / TAU) * k * (SIGMA_U - (SIGMA_X * y[1]) - self._sigma_b)) # edo flux de neutrons
])

def compute_neutrons_flow (xenon_ci, stop, title):
  # default values
  T0 = 0
  TIME_INTERVAL = 10 # 10s
  STOP = stop
  FLOW_CI = [1.0, xenon_ci, 10e10] # [I(T_0), X(T_0), PHI[T_0]]

  title = title
  x_label = "temps (h)"
  y_label = "Abondance"
  legends = ['Iode', 'Xénon', 'Flux de neutrons']

  isotope_abundance_rk4 = NeutronsFlow(title, y_label, x_label, legends, neutrons_flow_edo, T0, FLOW_CI, TIME_INTERVAL, STOP)
  isotope_abundance_rk4.resolve()
  isotope_abundance_rk4.graph()

def command_line ():
  command_line_questions = [
    {
      "type": "list",
      "name": "simu-tchernobyl",
      "message": "Simulation Tchernobyl en ligne de commande",
      "choices": [
        "Simuler l'abondance d'isotopes dans le réacteur (iode et xénon)"
      ]
    }
  ]

  command_line_answers = prompt(command_line_questions)
  command_line_answer = command_line_answers["simu-tchernobyl"]

  if (command_line_answer == "Simuler l'abondance d'isotopes dans le réacteur (iode et xénon)"):
    abundance_category()

def abundance_category ():
  abundances_questions = [
    {
      "type": "list",
      "name": "isotopes-abundance",
      "message": "Abondance d'isotopes dans le réacteur (iode et xénon), flux initial: 3e13",
      "choices": [
        "Après 2 jours - quantité initiale de xénon : 0",
        "Après 5 jours - quanité initiale de xénon : 2e15",
        "Après 5 jours - quantité initiale de xénon : 2e15, flux nul après 3 jours",
        "Flux de neutrons"
      ]
    }
  ]

  abundance_answers = prompt(abundances_questions)
  abundance_answer = abundance_answers["isotopes-abundance"]

  if (abundance_answer == "Après 2 jours - quantité initiale de xénon : 0"):
    # 1. Quantité de xénon initiale : 0.0
    # Temps de simulation : 2 jours
    stable_values()
    compute_isotopes_abundance(
      xenon_ci=0.0, 
      stop=day_to_seconds(2), 
      title="Abondance d'iode et de xénon entre 0 et 2 jours, Xénon au départ : 0"
    )
    return

  if (abundance_answer == "Après 5 jours - quanité initiale de xénon : 2e15"):
    # 2. Quantité de xénon initiale : 2e15
    # Temps de simulation : 5 jours
    compute_isotopes_abundance(
      xenon_ci=2e15, 
      stop=day_to_seconds(5), 
      title="Abondance d'iode et de xénon entre 0 et 5 jours, Xénon au départ : 2e15"
    )
    return

  if (abundance_answer == "Après 5 jours - quantité initiale de xénon : 2e15, flux nul après 3 jours"):
    # 3. Quantité de xénon initiale : 2e15
    # Temps de simulation : 5 jours
    # Flux après 3 jours : 0
    compute_isotopes_abundance(
      xenon_ci=2e15, 
      stop=day_to_seconds(5), 
      title="Abondance d'iode et de xénon entre 0 et 5 jours, Xénon au départ : 2e15, Flux = 0 après 3 jours",
      modify_flow=True,
      day_of_modification=3,
      next_flow=0
    )
    return

  if (abundance_answer == "Flux de neutrons"):
    compute_neutrons_flow(
      xenon_ci=0,
      stop=day_to_seconds(10),
      title="Flux de neutrons - stabilisation"
    )
    return

if __name__ == "__main__":
  start_questions = [
    {
      "type": "list",
      "name": "simu-tchernobyl",
      "message": "Simulation Tchernobyl",
      "choices": [
        "Ligne de commande",
        "GUI"
      ]
    }
  ]
  
  start_answers = prompt(start_questions)
  start_answer = start_answers["simu-tchernobyl"]

  if (start_answer == "Ligne de commande"):
    command_line()
  elif (start_answer == "GUI"):
    pass
    # Lancer l'interface graphique