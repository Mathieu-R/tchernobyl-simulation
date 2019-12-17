import matplotlib
import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
from matplotlib.widgets import Slider
from matplotlib.figure import Figure
from matplotlib import style

from constants import SIGMA_B_MIN

matplotlib.use("TkAgg")
style.use('seaborn-whitegrid')

PLOT_TIME_REFRESH = 1000 # 1000ms = 1s
DATA_TIME_REFRESH = 3600 # 3600s = 1h

class PlotAnimation(FigureCanvasTkAgg):
  def __init__(self, tk_root):
    self._figure = Figure(dpi=100)
    # lie le plot à la frame tkinter
    super().__init__(self._figure, tk_root)

    self._x_label = "Temps (h)"
    self._y_label = "Flux / Abondance"

    self._edo_legends = ['Iode', 'Xénon', 'Flux de neutrons'],

    self._axes = self._figure.add_subplot(111, xlabel=self._x_label, ylabel=self._y_label, yscale="log")
    self.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # https://github.com/matplotlib/matplotlib/issues/1656
    self._animation = animation.FuncAnimation(
      self._figure, 
      self.update,
      interval=PLOT_TIME_REFRESH
    )

    axcolor = 'lightgoldenrodyellow'
    axfreq = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
    self._slider = Slider(axfreq, 'Barres de contrôles', 0.1, 30.0, valinit=SIGMA_B_MIN)

    self._simulation = None
    self._slider = None

    plt.show()

  def update(self, interval):
    # si aucune simulation ne tourne, 
    # stop la mise à jour du plot
    if not self._simulation:
      return

    #self._end_slice = int(self._start_slice + (DATA_TIME_REFRESH / self._time_interval))

    # lis la valeur de sigma_b sur le slider
    sigma_b = self._slider.val

    # simule les EDO sur la sous-intervalle (1h par exemple)
    self._simulation.resolve()

    # récupère les données
    time_set = self._simulation.get_time_set()[:self._end_slice]
    y_set = self._simulation.get_y_set()[:self._end_slice]

    self._axes.clear()
    self._axes.plot(time_set, y_set, visible=True, linewidth=1)

    # reset stuff
    self._axes.set_xlabel(self._x_label)
    self._axes.set_ylabel(self._y_label)
    self._axes.set_yscale("log")
    self._axes.legend(self._edo_legends, loc="upper right")

    self._axes.relim()
    self._axes.autoscale_view()

    # redraw canvas
    self.draw_idle()

    #self._start_slice += (DATA_TIME_REFRESH / self._time_interval)

  def animate(self, simulation, time_interval, slider):
    self._simulation = simulation
    self._slider = slider
    self._time_interval = time_interval
    self._start_slice = 0