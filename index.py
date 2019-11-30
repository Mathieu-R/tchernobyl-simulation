#!/usr/bin/env python3
import numpy as np
from decimal import Decimal
from edo_solver.rk4 import RK4Method
from PyInquirer import prompt, print_json

from utils import day_to_seconds
from constants import GAMMA_I, GAMMA_X, SIGMA_F, LAMBDA_I, LAMBDA_X, SIGMA_I, SIGMA_X

def isotopes_abundance_edo (t, y, modify_flow, day_of_modification, next_flow):
  # Default initial flow of neutrons
  phi = 3e13

  # après 3 jours
  if (modify_flow and t >= day_to_seconds(day_of_modification)): 
    phi = next_flow

  # y = [I, X]
  return np.array([
    (GAMMA_I * SIGMA_F * phi) - (LAMBDA_I * y[0]) - (SIGMA_I * y[0] * phi), # edo iode
    (GAMMA_X * SIGMA_F * phi) + (LAMBDA_I * y[0]) - (SIGMA_X * y[1] * phi) - (LAMBDA_X * y[1]) # edo xénon
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
  phi = 3e13

  I = GAMMA_I * SIGMA_F * phi / (LAMBDA_I + SIGMA_I)
  X = (1 / ((SIGMA_X * phi) + LAMBDA_X)) * (GAMMA_X * SIGMA_F * phi) + (LAMBDA_I * I)
  print("Après 2 jours, pour un flux de 3e13 :")
  print('Iode:', '%.2E' % Decimal(I),' Xénon:', '%.2E' % Decimal(X))


def start ():
  main_questions = [
    {
      "type": "list",
      "name": "simu-tchernobyl",
      "message": "Simulation Tchernobyl",
      "choices": [
        "Simuler l'abondance d'isotopes dans le réacteur (iode et xénon)"
      ]
    }
  ]

  main_answers = prompt(main_questions)
  main_answer = main_answers["simu-tchernobyl"]

  if (main_answer == "Simuler l'abondance d'isotopes dans le réacteur (iode et xénon)"):
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
        "Après 5 jours - quantité initiale de xénon : 2e15, flux nul après 3 jours"
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

if __name__ == "__main__":
  start()
