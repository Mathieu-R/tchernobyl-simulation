from .rk4 import RK4Method
from constants import SIGMA_B_MIN

class NeutronsFlow(RK4Method):
  def __init__(self, title, y_label, x_label, edo_legends, edo, t0, ci, time_interval, stop, modify_flow=False, day_of_flow_modification=None, next_flow=None):
    self._sigma_b = SIGMA_B_MIN
    super().__init__(title, y_label, x_label, edo_legends, edo, t0, ci, time_interval, stop, modify_flow=modify_flow, day_of_flow_modification=day_of_flow_modification, next_flow=next_flow)

