import matplotlib.pyplot as plt
import numpy as np
from random import randint

class EDONumericalResolution:
  def __init__(self, title, edo, t0, ci, time_interval, stop):
    # title of the graph
    self._title = title
    # function that return [y' = CI, y'' = EDO] as a matrix
    self._edo = edo
    self._t0 = t0
    # [y(0), y'(0)]
    self._ci = ci
    self._time_interval = time_interval
    self._stop = stop
    self._time_set = [self._t0]
    self._y_set = [self._ci[:]]
    self._edo_legends = ['position [m]', 'vitesse [m/s]']
    self._colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple']

  def resolve(self):
    raise NotImplemented

  def graph(self):
    for index, column in enumerate(self._y_set):
      color = self._colors[randint(0, len(self._colors) - 1)]
      plt.plot(self._time_set, column, f"{color}")
    
    plt.title(self._title)
    # https://stackoverflow.com/questions/44632571/pyplot-legend-only-displaying-one-letter?noredirect=1&lq=1
    plt.legend(self._edo_legends, loc="upper right")
    plt.xlabel("time [s]") 
    plt.ylabel("y")
    plt.show()