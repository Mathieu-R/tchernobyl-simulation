import matplotlib.pyplot as plt
import numpy as np
from random import randint

class EDONumericalResolution:
  def __init__(self, title, y_label, x_label, edo_legends, edo, t0, ci, time_interval, stop):
    # title of the graph
    self._title = title
    self._y_label = y_label
    self._x_label = x_label
    # function that return [y' = CI, y'' = EDO] as a matrix
    self._edo = edo
    self._t0 = t0
    # [y(0), y'(0)]
    self._ci = ci
    self._time_interval = time_interval
    self._stop = stop
    self._time_set = []
    self._y_set = []
    self._edo_legends = edo_legends
    self._colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple']

  def resolve(self):
    raise NotImplemented

  def graph(self): 
    plt.plot(self._time_set, self._y_set)
    plt.title(self._title)
    # https://stackoverflow.com/questions/44632571/pyplot-legend-only-displaying-one-letter?noredirect=1&lq=1
    plt.legend(self._edo_legends, loc="upper right")
    plt.xlabel(self._x_label) 
    plt.ylabel(self._y_label)
    plt.show()

class RK4Method(EDONumericalResolution):
  def derivatives(self, tn, y):
    k1 = self._edo(tn, y)
    k2 = self._edo(tn + (self._time_interval / 2), y + ((self._time_interval / 2) * k1))
    k3 = self._edo(tn + (self._time_interval / 2), y + ((self._time_interval / 2) * k2))
    k4 = self._edo(tn + self._time_interval, y + (self._time_interval * k3))
    return (k1 + 2*k2 + 2*k3 + k4)

  def resolve(self):
    y = np.array(self._ci) # [I(0), X(0)]

    self._time_set.append(self.second_to_hour(self._t0)) 
    self._y_set.append(y.copy())

    # increment because we want to calculate
    # approximate solution from t + step
    # (we already have t = t_0 given by CI)
    self._t0 += self._time_interval

    # range function for float
    # self._stop + self._time_interval because self._stop is excluded
    for t in np.arange(self._t0, self._stop + self._time_interval, self._time_interval):
      # resolve each first order edo (e.g. position (x'), speed (v'))
      y += (self._time_interval / 6) * self.derivatives(t, y)

      self._time_set.append(self.second_to_hour(t))
      self._y_set.append(y.copy())
    
    # matrix transposition
    self._y_set = np.array(self._y_set)

  def second_to_hour (self, seconds):
    hours = seconds / 3600
    return hours