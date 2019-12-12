from .rk4 import RK4Method
from constants import PHI
from utils import day_to_seconds

class IsotopesAbundance(RK4Method):
  def __init__(self, title, y_label, x_label, edo_legends, edo, t0, ci, time_interval, stop, modify_flow=False, day_of_flow_modification=None, next_flow=None):
    self._modify_flow = modify_flow
    self._day_of_flow_modification = day_of_flow_modification
    self._next_flow = next_flow
    self._phi = PHI

    super().__init__(title, y_label, x_label, edo_legends, edo, t0, ci, time_interval, stop)

  def derivatives(self, tn, y):
    # après 3 jours
    if (self._modify_flow and tn >= day_to_seconds(self._day_of_flow_modification)): 
      self._phi = self._next_flow

    k1 = self._edo(self, tn, y)
    k2 = self._edo(self, tn + (self._time_interval / 2), y + ((self._time_interval / 2) * k1))
    k3 = self._edo(self, tn + (self._time_interval / 2), y + ((self._time_interval / 2) * k2))
    k4 = self._edo(self, tn + self._time_interval, y + (self._time_interval * k3))
    return (k1 + 2*k2 + 2*k3 + k4)