#!/usr/bin/env python3.8
import numpy as np
import matplotlib.pyplot as plt

from PyInquirer import prompt, print_json
from command_line.cli import command_line
from gui.gui import GraphicInterface

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
    # Lancer l'interface graphique
    GraphicInterface()