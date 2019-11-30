import matplotlib.pyplot as plt
import numpy as np

from .solver import EDONumericalResolution

class RK4Method(EDONumericalResolution):
  def derivatives(self, tn, y, modify_flow, day_of_flow_modification, next_flow):
    k1 = self._edo(tn, y, modify_flow, day_of_flow_modification, next_flow)
    k2 = self._edo(tn + (self._time_interval / 2), y + ((self._time_interval / 2) * k1), modify_flow, day_of_flow_modification, next_flow)
    k3 = self._edo(tn + (self._time_interval / 2), y + ((self._time_interval / 2) * k2), modify_flow, day_of_flow_modification, next_flow)
    k4 = self._edo(tn + self._time_interval, y + (self._time_interval * k3), modify_flow, day_of_flow_modification, next_flow)
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
      y += (self._time_interval / 6) * self.derivatives(t, y, self._modify_flow, self._day_of_flow_modification, self._next_flow)

      self._time_set.append(self.second_to_hour(t))
      self._y_set.append(y.copy())
    
    self._y_set = np.array(self._y_set)

  def second_to_hour (self, seconds):
    hours = seconds / 3600
    return hours
