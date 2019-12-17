from .rk4 import RK4Method
from utils import day_to_seconds
from constants import PHI

class IsotopesAbundance(RK4Method):
  def __init__(self, edo, ci, full_time_range, time_step):
    self.modify_flow = modify_flow
    self.day_of_flow_modification = day_of_flow_modification
    self.next_flow = next_flow
    self.phi = PHI

    super().__init__(edo, ci, full_time_range, time_step)

  def derivatives(self, tn, y):
    # après 3 jours
    if (self.modify_flow and tn >= day_to_seconds(self.day_of_flow_modification)): 
      self.phi = self.next_flow

    k1 = self.edo(self, tn, y)
    k2 = self.edo(self, tn + (self.time_step / 2), y + ((self.time_step / 2) * k1))
    k3 = self.edo(self, tn + (self.time_step / 2), y + ((self.time_step / 2) * k2))
    k4 = self.edo(self, tn + self.time_step, y + (self.time_step * k3))
    return (k1 + 2*k2 + 2*k3 + k4)