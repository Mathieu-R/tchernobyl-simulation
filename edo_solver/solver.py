import matplotlib.pyplot as plt
import numpy as np

class EDONumericalResolution:
  def __init__(self, edo, t0, ci, time_interval, stop):
    # function that return [y' = CI, y'' = EDO] as a matrix
    self._edo = edo
    self._t0 = t0
    # [y(0), y'(0)]
    self._ci = ci
    self._time_interval = time_interval
    self._stop = stop

    # keep track of data
    self._time_set = []
    self._y_set = []

  def resolve(self):
    raise NotImplemented

  def graph(self, title, edo_legends, x_label, y_label): 
    plt.plot(self._time_set, self._y_set)
    plt.title(title)
    # https://stackoverflow.com/questions/44632571/pyplot-legend-only-displaying-one-letter?noredirect=1&lq=1
    plt.legend(edo_legends, loc="upper right")
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.yscale('log')
    plt.show()

  def graph_sigma_b(self):
    plt.plot(self._time_set, np.array(self._sigma_b_set))
    plt.title("Barres de contrôle")
    # https://stackoverflow.com/questions/44632571/pyplot-legend-only-displaying-one-letter?noredirect=1&lq=1
    plt.legend(["Section efficace des neutrons avec les barres de contrôle"], loc="upper right")
    plt.xlabel(self._x_label)
    plt.ylabel("Sigma B")
    plt.show()

  # def set_t0(self, t0):
  #   self._t0 = t0

  # def set_ci(self, ci):
  #   self._ci = ci 

  # def set_time_interval(self, time_interval):
  #   self._time_interval = time_interval

  # def set_stop(self, stop):
  #   self._stop = stop

  def get_time_set(self):
    return self._time_set

  def get_y_set(self):
    return self._y_set