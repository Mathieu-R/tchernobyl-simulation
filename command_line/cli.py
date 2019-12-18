import numpy as np

from decimal import Decimal
from edo_solver.rk4 import RK4Method
from edo_solver.neutrons_flow import NeutronsFlow
from edo_solver.isotopes_abundance import IsotopesAbundance
from edo_solver.edo import isotopes_abundance_edo, neutrons_flow_edo
from PyInquirer import prompt, print_json

from utils import day_to_seconds, seconds_to_hour
from constants import (GAMMA_I, GAMMA_X, SIGMA_F, LAMBDA_I, LAMBDA_X, SIGMA_I, SIGMA_X, 
  PHI, TAU, k, SIGMA_U, SIGMA_B_MAX, SIGMA_B_MIN, SIGMA_B_STEP, STABLE_FLOW, FLOW_START, FLOW_DROP)

def compute_isotopes_abundance (xenon_ci, stop, title, modify_flow = False, day_of_flow_modification = None, next_flow = None):
  # default values
  T0 = 0
  TIME_INTERVAL = 10 # 10s
  STOP = stop
  ISOTOPES_CI = [1.0, xenon_ci] # [I(T_0), X(T_0)]

  title = title
  x_label = "temps (h)"
  y_label = "Abondance"
  legends = ['Iode', 'Xénon']

  full_time_range = np.arange(T0, STOP + TIME_INTERVAL, TIME_INTERVAL)

  isotope_abundance_rk4 = IsotopesAbundance(isotopes_abundance_edo, ISOTOPES_CI, full_time_range, TIME_INTERVAL, modify_flow, day_of_flow_modification, next_flow)
  isotope_abundance_rk4.resolve()
  isotope_abundance_rk4.graph(title, legends, x_label, y_label)

# valeur stables de xénon et iode après 2 jours
def stable_values ():
  phi = PHI

  I = (GAMMA_I * SIGMA_F * phi) / (LAMBDA_I + SIGMA_I * phi)
  X = ((GAMMA_X * SIGMA_F * phi) + (LAMBDA_I * I)) / ((SIGMA_X * phi) + (LAMBDA_X))
  print("Après 2 jours, pour un flux de 3e13 :")
  print('Iode:', '%.2E' % Decimal(I),' Xénon:', '%.2E' % Decimal(X))

def compute_neutrons_flow (xenon_start, stop, title):
  # default values
  T0 = 0
  TIME_INTERVAL = 10 # 10s
  STOP = stop
  FLOW_CI = [1.0, xenon_start, FLOW_START] # [I(T_0), X(T_0), PHI[T_0]]

  title = title
  x_label = "temps (h)"
  y_label = "Abondance"
  legends = ['Iode', 'Xénon', 'Flux de neutrons']

  full_time_range = np.arange(T0, STOP + TIME_INTERVAL, TIME_INTERVAL)

  isotope_abundance_rk4 = NeutronsFlow(neutrons_flow_edo, FLOW_CI, full_time_range, TIME_INTERVAL)
  isotope_abundance_rk4.resolve()
  isotope_abundance_rk4.graph(title, legends, x_label, y_label)
  isotope_abundance_rk4.graph_sigma_b(x_label)

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
      day_of_flow_modification=3,
      next_flow=0
    )
    return

def command_line ():
  command_line_questions = [
    {
      "type": "list",
      "name": "simu-tchernobyl",
      "message": "Simulation Tchernobyl en ligne de commande",
      "choices": [
        "Simuler l'abondance d'isotopes dans le réacteur (iode et xénon)",
        "Simuler le flux de neutrons"
      ]
    }
  ]

  command_line_answers = prompt(command_line_questions)
  command_line_answer = command_line_answers["simu-tchernobyl"]

  if (command_line_answer == "Simuler l'abondance d'isotopes dans le réacteur (iode et xénon)"):
    abundance_category()
  
  elif (command_line_answer == "Simuler le flux de neutrons"):
    compute_neutrons_flow(
      xenon_start=0,
      stop=day_to_seconds(20),
      title="Flux de neutrons - stabilisation"
    )