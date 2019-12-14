import matplotlib
import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
from matplotlib.figure import Figure
from matplotlib import style

matplotlib.use("TkAgg")
style.use('seaborn-whitegrid')

PLOT_TIME_REFRESH = 1000 # 1s
DATA_TIME_REFRESH = 86400 # 1h

class PlotAnimation(FigureCanvasTkAgg):
  def __init__(self, tk_root):
    self._figure = Figure(dpi=100)
    # lie le plot à la frame tkinter
    super().__init__(self._figure, tk_root)

    x_label = "Temps (h)"
    y_label = "Flux / Abondance"

    self._axes = self._figure.add_subplot(111, xlabel=x_label, ylabel=y_label, yscale="log")
    self.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    self._animation = None

  def update(self, interval):
    print("loop")
    # récupère les données
    time_set = self._simulation.get_time_set()
    y_set = self._simulation.get_y_set()

    # La méthode update n'est pas lancée par animate
    print(y_set, time_set)

    self._axes.clear()
    self._axes.plot(time_set, y_set, visible=True, linewidth=1)
    self._axes.legend(fancybox=True)

    self._axes.relim()
    self._axes.autoscale_view()

    # redraw canvas
    self.draw_idle()

  def animate(self, simulation):
    print("animate")
    self._simulation = simulation
    
    # https://github.com/matplotlib/matplotlib/issues/1656
    self._animation = animation.FuncAnimation(
      self._figure, 
      self.update,
      interval=1000
    )

    plt.show()

    # self._edo_legends = ['Iode', 'Xénon', 'Flux de neutrons'],
    # self._axes.legend(self._edo_legends, loc="upper right")