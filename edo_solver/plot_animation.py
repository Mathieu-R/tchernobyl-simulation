import matplotlib.pyplot as plt
import matplotlib.animation as animation

from edo_solver.edo import neutrons_flow_edo 
from edo_solver.neutrons_flow import NeutronsFlow
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PlotAnimation():
  def __init__(self, time_interval, time_refresh, ci, simulation_time, tk_root, mpl_figure, mpl_axes, line):
    # début de l'évaluation de l'edo
    self._t0 = 0
    # temps actuel de la simulation
    self._t = 0
    # intervalle d'évaluation de l'edo
    self._time_interval = time_interval
    # temps passé dans la simulation 
    # après chaque rafraichissement de l'animation
    self._time_refresh = time_refresh
    # temps d'une loop de simulation
    self._stop = time_refresh / time_interval
    # durée complète de la simulation
    self._simulation_time = simulation_time
    # conditions initiales (pour chaque loop)
    self._ci = ci
    
    self._tk_root = tk_root
    self._mpl_figure = mpl_figure
    self._mpl_axes = mpl_axes
    self._line = line

  def init_background(self):
    self._line.set_data([], [])
    return self._line,

  def update(self, interval):
    print("loop")
    # lance une boucle
    # résolution des edo
    self._simulation.resolve()

    # récupère les données
    time_set = self._simulation.get_time_set()
    y_set = self._simulation.get_y_set()

    # plot les données
    #self._line.set_data(time_set, y_set)
    self._mpl_axes.clear()
    self._mpl_axes.plot(time_set, y_set)

    # change les données pour la prochaine loop
    self._simulation.set_ci(y_set[len(y_set) - 1])

    self._t += self._stop
    self._simulation.set_t0(self._t)

    self._stop += self._stop
    self._simulation.set_stop(self._stop)

    return self._line,

  def animate(self):
    print("animate")
    self._simulation = NeutronsFlow(
      neutrons_flow_edo, 
      self._t0, 
      self._ci, 
      self._time_interval, 
      self._stop
    )
    
    animation.FuncAnimation(
      self._mpl_figure, 
      self.update, 
      init_func=self.init_background, 
      frames=200, 
      interval=1000,
      blit=True
    )


