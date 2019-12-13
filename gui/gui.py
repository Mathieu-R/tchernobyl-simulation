import math
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import tkinter as tk
#from ttkthemes import themed_tk
from tkinter import ttk

matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from pandas import DataFrame

from edo_solver.edo import neutrons_flow_edo 
from edo_solver.neutrons_flow import NeutronsFlow

from edo_solver.plot_animation import PlotAnimation
from utils import day_to_seconds, hour_to_seconds
from constants import FLOW_START, TIME_INTERVAL

class GraphicInterface():
  def __init__(self):
    # fenêtre principale
    self._root = tk.Tk()
    self._root.title("Simulation du réacteur d'une centrale nucléaire") 

    launch_simulation_button = tk.Button(self._root, text="Lancer la simulation", command=self.plot_neutrons_flow)
    launch_simulation_button.grid(row=0, column=0)
    
    manage_control_bars_button = tk.Button(self._root, text="Gérer les barres de contrôle", command=self.control_bars)
    manage_control_bars_button.grid(row=0, column=1)

    quit_button = tk.Button(self._root, text="Quit", command=self.quit)
    quit_button.grid(row=0, column=2)

    # (à placer dans le canvas) contiendra le graph 
    self._figure = Figure(figsize=(12, 7), dpi=100)
    # Axes
    self._axes = self._figure.add_subplot(111)
    # Line2D
    self._line, = self._axes.plot([], [], lw=1)

    self._edo_legends = ['Iode', 'Xénon', 'Flux de neutrons'],
    self._x_label = "temps (h)",
    self._y_label = "Flux / Abondance",

    self._axes.legend(self._edo_legends, loc="upper right")
    self._axes.set_xlabel(self._x_label)
    self._axes.set_ylabel(self._y_label)
    self._axes.set_yscale('log')

    # canvas (afin de dessiner le graph dans tkinter)
    self._canvas = FigureCanvasTkAgg(self._figure, self._root)
    #self._canvas.draw()
    self._canvas.get_tk_widget().grid(row=1, column=0)

    # Indique si la simulation est lancée
    self._started = False

    # edo simulation
    self._simulation = None
    
    self._root.mainloop()

  def plot_neutrons_flow(self):
    # Lancement de la simulation
    if not self._started:   
      FLOW_CI = [1.0, 2e15, FLOW_START] # [I(T_0), X(T_0), PHI[T_0]]

      self._simulation = NeutronsFlow(
        edo=neutrons_flow_edo, 
        t0=0,
        ci=FLOW_CI,
        time_interval=10,
        stop=hour_to_seconds(100)
      )

      animation = PlotAnimation(
        time_interval=10, 
        time_refresh=3600, 
        ci=FLOW_CI, 
        simulation_time=hour_to_seconds(100),
        simulation=self._simulation,
        tk_root = self._root,
        mpl_figure = self._figure,
        mpl_axes = self._axes,
        line = self._line
      )
      animation.animate()
      self._started = True

  def on_stop_simulation_button_click (self):
    self._paused = True

  def control_bars(self):
    flow_control_bars = tk.Toplevel(self._root)

    title = tk.Label(
      flow_control_bars, 
      text="Commandes pour le graphe du flux de neutron",
      font=("Helvetica", 15)
    )
    title.grid()

    subtitle = tk.Label(flow_control_bars, text="Valeur des barres de ralentissement")
    subtitle.grid()

    scale = tk.Scale(
      flow_control_bars, 
      variable=var, 
      from_=0.2, 
      to=0.1, 
      resolution = 0.0001, 
      length=200,
      command=self.update_bars
    )
    scale.grid()

  def update_bars(self, sigma_b):
    self._simulation.set_sigma_b(sigma_b)

  def quit(self):
    self._root.quit()
    self._root.destroy()