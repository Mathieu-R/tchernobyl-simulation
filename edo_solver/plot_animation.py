import matplotlib
import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
from matplotlib.widgets import Slider
from matplotlib.figure import Figure
from matplotlib import style

from utils import seconds_to_hour
from constants import SIGMA_B_MIN

matplotlib.use("TkAgg")
style.use('seaborn-whitegrid')

PLOT_TIME_REFRESH = 1000 # 1000ms = 1s
DATA_TIME_REFRESH = 3600 # 3600s = 1h

class PlotAnimation(FigureCanvasTkAgg):
  def __init__(self, tk_root):
    self.figure = Figure(dpi=100)
    # lie le plot à la frame tkinter
    super().__init__(self.figure, tk_root)

    self.x_label = "Temps (h)"
    self.y_label = "Flux / Abondance"

    self.edo_legends = ['Iode', 'Xénon', 'Flux de neutrons'],

    self.axes = self.figure.add_subplot(111, xlabel=self.x_label, ylabel=self.y_label, yscale="log")
    self.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # # https://github.com/matplotlib/matplotlib/issues/1656
    # self.animation = animation.FuncAnimation(
    #   self.figure, 
    #   self.update,
    #   interval=PLOT_TIME_REFRESH
    # )

    axcolor = 'lightgoldenrodyellow'
    #axfreq = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
    #self.slider = Slider(axfreq, 'Barres de contrôles', 0.1, 30.0, valinit=SIGMA_B_MIN)
    #self.slider.on_changed(self.update_sigma_b)

    self.simulation = None
    self.slider = None

    plt.show()

  def update_sigma_b(self, sigma_b):
    self.simulation.sigma_b = sigma_b

  def update(self, i):
    print(i)
    # si aucune simulation ne tourne, 
    # stop la mise à jour du plot
    if not self.simulation:
      i = 0
      return

    # lis la valeur de sigma_b sur le slider
    #sigma_b = self.slider.val

    sub_interval_start = i * (DATA_TIME_REFRESH)
    sub_interval_end = (i + 1) * (DATA_TIME_REFRESH)

    print(sub_interval_start, sub_interval_end)
    print(len(self.simulation.y_set))

    # sous-intervalle
    time_range = np.arange(sub_interval_start, sub_interval_end, self.simulation.time_step)

    # simule les EDO sur la sous-intervalle (1h par exemple)
    self.simulation.resolve(sub_interval=time_range)

    # mise à jour des CI
    self.simulation.ci = self.simulation.y_set[sub_interval_end]

    # récupère les données
    time_set = self.simulation.full_time_range[:sub_interval_end]
    time_set_in_hours = map(lambda t: seconds_to_hour(t), time_set)

    y_set = self.simulation.y_set[:sub_interval_end]

    self.axes.clear()
    self.axes.plot(time_set, y_set, visible=True, linewidth=1)

    # reset stuff
    self.axes.set_xlabel(self.x_label)
    self.axes.set_ylabel(self.y_label)
    self.axes.set_yscale("log")
    self.axes.legend(self.edo_legends, loc="upper right")

    self.axes.relim()
    self.axes.autoscale_view()

    # redraw canvas
    self.draw_idle()

  def animate(self, simulation, time_end):
    self.simulation = simulation

    # https://github.com/matplotlib/matplotlib/issues/1656
    self.animation = animation.FuncAnimation(
      self.figure, 
      self.update,
      frames=range(1, time_end),
      interval=PLOT_TIME_REFRESH,
      blit=True,
      repeat=False
    )