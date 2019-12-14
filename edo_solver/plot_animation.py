import matplotlib
import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
from matplotlib.figure import Figure
from matplotlib import style

matplotlib.use("TkAgg")
style.use('seaborn-whitegrid')

class PlotAnimation(FigureCanvasTkAgg):
  def __init__(self, tk_root):
    self._figure = Figure(dpi=100)
    super().__init__(self._figure, tk_root)

    x_label = "Temps (h)"
    y_label = "Flux / Abondance"

    self._axes = self._figure.add_subplot(111, xlabel=x_label, ylabel=y_label, yscale="log")
    self.get_tk_widget().grid(row=0, column=0, sticky="nsew")
    #self.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

  # def __init__(self, time_interval, time_refresh, ci, simulation_time, simulation, tk_root, mpl_figure, mpl_axes, line):
  #   # début de l'évaluation de l'edo
  #   self._t0 = 0
  #   # temps actuel de la simulation
  #   #self._t = 0
  #   # intervalle d'évaluation de l'edo
  #   self._time_interval = time_interval
  #   # temps passé dans la simulation 
  #   # après chaque rafraichissement de l'animation
  #   #self._time_refresh = time_refresh
  #   # temps d'une loop de simulation
  #   #self._stop = time_refresh / time_interval
  #   # durée complète de la simulation
  #   self._simulation_time = simulation_time
  #   # conditions initiales (pour chaque loop)
  #   self._ci = ci
  #   # edo simulation
  #   self._simulation = simulation
    
  #   self._tk_root = tk_root
  #   self._mpl_figure = mpl_figure
  #   self._mpl_axes = mpl_axes
  #   self._line = line

  def update(self, interval):
    # lance une boucle
    # résolution des edo
    #self._simulation.resolve()

    # récupère les données
    time_set = self._simulation.get_time_set()
    y_set = self._simulation.get_y_set()

    # La méthode update n'est pas lancée par animate
    print(y_set, time_set)

    self._axes.clear()
    self._axes.plot(time_set, y_set, visible=True, linewidth=1)
    self._axes.legend(fancybox=True)

    # redraw canvas
    self.draw_idle()

    # # change les données pour la prochaine loop
    # self._simulation.set_ci(y_set[len(y_set) - 1])

    # self._t += self._stop
    # self._simulation.set_t0(self._t)

    # self._stop += self._stop
    # self._simulation.set_stop(self._stop)

  def animate(self, simulation):
    self._simulation = simulation
    self._simulation.resolve()
    
    animation.FuncAnimation(
      self._figure, 
      self.update,
      interval=1000
    )

    # self._edo_legends = ['Iode', 'Xénon', 'Flux de neutrons'],
    # self._axes.legend(self._edo_legends, loc="upper right")