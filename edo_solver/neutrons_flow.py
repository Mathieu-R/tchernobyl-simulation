from .rk4 import RK4Method
from constants import SIGMA_B_MIN

class NeutronsFlow(RK4Method):
  def __init__(self, title, y_label, x_label, edo_legends, edo, t0, ci, time_interval, stop):
    self._sigma_b = SIGMA_B_MIN
    self._timer_started = False
    self._timer_start = 0
    super().__init__(title, y_label, x_label, edo_legends, edo, t0, ci, time_interval, stop)


