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
style.use('seaborn-whitegrid')

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
    
    self.axes.legend()

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
    # si aucune simulation ne tourne, 
    # stop la mise à jour du plot
    # if not self.simulation:
    #   return

    if (i > self.time_end):
      return

    time_step = self.simulation.time_step

    sub_interval_start = (i - 1) * (DATA_TIME_REFRESH)
    # incrémente car la dernière valeur n'est pas prise en compte
    sub_interval_end = (i) * (DATA_TIME_REFRESH) 

    # sous-intervalle
    time_range = np.arange(sub_interval_start, sub_interval_end + time_step, time_step)

    # simule les EDO sur la sous-intervalle (1h par exemple)
    self.simulation.resolve(sub_interval=time_range)
    
    last_index_value = int(sub_interval_end / time_step)
    #print(last_index_value)

    # mise à jour des CI
    self.simulation.ci = self.simulation.y_set[last_index_value]

    # récupère les données
    time_set = self.simulation.full_time_range[:last_index_value]
    time_set_in_hours = np.fromiter(map(lambda t: seconds_to_hour(t), time_set), dtype=np.float)

    # should have 1 line for each data (iodine, xenon, neutrons flow)
    iodine = self.simulation.y_set[:last_index_value, 0]
    xenon = self.simulation.y_set[:last_index_value, 1]
    neutrons_flow = self.simulation.y_set[:last_index_value, 2]

    #self.axes.clear()
    #self.axes.plot(time_set, y_set, visible=True, linewidth=1)
    self.iodine.set_data(time_set_in_hours, iodine)
    self.xenon.set_data(time_set_in_hours, xenon)
    self.neutrons_flow.set_data(time_set_in_hours, neutrons_flow)

    self.axes.relim()
    self.axes.autoscale_view()

    # redraw canvas
    #self.draw_idle()

    return self.iodine, self.xenon, self.neutrons_flow

  def animate(self, simulation, time_end):
    self.simulation = simulation
    self.time_end = time_end

    plt.xlim(0, time_end)

    # https://github.com/matplotlib/matplotlib/issues/1656
    self.animation = animation.FuncAnimation(
      self.figure, 
      self.update,
      # BUG: devrait aller jusque i = 100 (valeur de time_end si on choisi 100h de simulation)
      # mais il dépasse 100 => out_of_bounds index
      frames=range(1, time_end - 1),
      interval=PLOT_TIME_REFRESH,
      init_func=self.init,
      blit=True,
      repeat=True
    )

    #self.animation.save('simu.mp4', writer="ffmpeg")