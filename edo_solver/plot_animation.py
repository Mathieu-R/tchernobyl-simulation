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
from constants import SIGMA_B_MIN, SIGMA_B_MAX

matplotlib.use("TkAgg")
#style.use('seaborn-whitegrid')

PLOT_TIME_REFRESH = 1000 # 1000ms = 1s
DATA_TIME_REFRESH = 3600 # 3600s = 1h

class PlotAnimation(FigureCanvasTkAgg):
  def __init__(self, tk_root):
    self.figure = Figure(dpi=100)
    # lie le plot à la frame tkinter (crée un canvas)
    super().__init__(self.figure, tk_root)
    self.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    self.x_label = "Temps (h)"
    self.y_label = "Flux / Abondance"

    self.axes = self.figure.add_subplot(111, xlabel=self.x_label, ylabel=self.y_label, yscale="log")

    # données
    self.iodine, = self.axes.plot([], [], color="royalblue", label="Iode", lw=1)
    self.xenon, = self.axes.plot([], [], color="orange", label="Xénon", lw=1)
    self.neutrons_flow, = self.axes.plot([], [], color="green", label="Flux de neutrons", lw=1)
    
    self.axes.legend(loc="upper left", fancybox=True)

    self.simulation = None

    plt.show()
  
  def toggle(self, pause):
    if not self.simulation:
      return
    
    if pause:
      self.animation.event_source.stop()
    
    if not pause:
      self.animation.event_source.start()
  
  def stop(self):
    if not self.animation:
      return

    self.animation.event_source.stop()
    self.init()
    # force le redessinage du plot
    self.draw_idle()

  def init(self):
    # reset
    self.iodine.set_data([], [])
    self.xenon.set_data([], [])
    self.neutrons_flow.set_data([], [])
    return self.iodine, self.xenon, self.neutrons_flow,

  def update(self, i):
    print(i)

    if (i > self.time_end):
      return

    time_step = self.simulation.time_step

    sub_interval_start = (i - 1) * (DATA_TIME_REFRESH)
    sub_interval_end = (i) * (DATA_TIME_REFRESH) 

    # sous-intervalle
    # incrémente car la dernière valeur n'est pas prise en compte
    time_range = np.arange(sub_interval_start, sub_interval_end + time_step, time_step)

    # simule les EDO sur la sous-intervalle (1h par exemple)
    self.simulation.resolve(sub_interval=time_range)
    
    last_index_value = int(sub_interval_end / time_step)
    twenty_four_hours_index = int((24 * 3600) / time_step)
    twenty_four_hours = max(0, int(last_index_value - twenty_four_hours_index))
    #print(last_index_value)

    # mise à jour des CI
    self.simulation.ci = self.simulation.y_set[last_index_value]

    # récupère les données
    time_set = self.simulation.full_time_range[twenty_four_hours:last_index_value]
    time_set_in_hours = np.fromiter(map(lambda t: seconds_to_hour(t), time_set), dtype=np.float)

    print(twenty_four_hours, last_index_value, twenty_four_hours_index)

    iodine = self.simulation.y_set[twenty_four_hours:last_index_value, 0]
    xenon = self.simulation.y_set[twenty_four_hours:last_index_value, 1]
    neutrons_flow = self.simulation.y_set[twenty_four_hours:last_index_value, 2]

    self.iodine.set_data(time_set_in_hours, iodine)
    self.xenon.set_data(time_set_in_hours, xenon)
    self.neutrons_flow.set_data(time_set_in_hours, neutrons_flow)

    self.axes.relim()
    self.axes.autoscale_view()

    return self.iodine, self.xenon, self.neutrons_flow

  def animate(self, simulation, time_end):
    self.simulation = simulation
    self.time_end = time_end

    # https://github.com/matplotlib/matplotlib/issues/1656
    # NOTE: blitting est plus rapide mais empêche de redimensionner dynamiquement le plot
    self.animation = animation.FuncAnimation(
      self.figure, 
      self.update,
      frames=range(1, int(seconds_to_hour(time_end)) + 1),
      interval=PLOT_TIME_REFRESH,
      #init_func=self.init,
      #blit=True,
      repeat=False
    )

    self.draw_idle()