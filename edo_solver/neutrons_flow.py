from .rk4 import RK4Method
from constants import SIGMA_B_MIN, SIGMA_B_MAX, SIGMA_B_STEP, STABLE_FLOW, FLOW_DROP
from utils import seconds_to_hour
from decimal import Decimal

class NeutronsFlow(RK4Method):
  def __init__(self, edo, ci, full_time_range, time_step):
    # barres de contrôle
    self.sigma_b = SIGMA_B_MIN
    self.timer_started = False
    self.timer_start = 0
    self.sigma_b_set = [SIGMA_B_MIN]
    super().__init__(edo, ci, full_time_range, time_step)

  # y[0] : abondance d'iode
  # y[1] : abondance de xénon
  # y[2] : flux de neutrons
  def derivatives(self, tn, y):
    print(y)
    # Si le flux est plus ou moins stabilisé
    # On démarre un timer et on attend 24 heures
    # Après cela, on baisse le flux à 1% de sa valeur stable
    if (y[2] > STABLE_FLOW - 0.5E10 and y[2] < STABLE_FLOW + 0.5E10 and not self.timer_started):
      self.timer_started = True
      self.timer_start = tn

    if (self.timer_started and seconds_to_hour(tn - self.timer_start) >= 24):
      # Si le flux est plus bas que la valeur de drop
      # on diminue la section efficace des neutrons (sigma_b)
      # en veillant à que sigma_b ne descende pas en dessous de la valeur minimale
      if (y[2] < FLOW_DROP):
        new_sigma_b = max(SIGMA_B_MIN, self.sigma_b - SIGMA_B_STEP)
        self.sigma_b -= new_sigma_b
      
      # Si le flux est plus haut que la valeur de drop
      # on diminue la section efficace des neutrons (sigma_b)
      # en veillant à que sigma_b ne monte pas en dessus de la valeur minimale
      elif (y[2] > FLOW_DROP):
        new_sigma_b = min(SIGMA_B_MAX, self.sigma_b + SIGMA_B_STEP)
        self.sigma_b = new_sigma_b

    #if (y[2] > STABLE_FLOW - (1E10 / 1000)

    # Si le flux est plus bas que le flux stable
    # on diminue la section efficace des neutrons (sigma_b)
    # en veillant à que sigma_b ne descende pas en dessous de la valeur minimale
    if (y[2] < STABLE_FLOW):
      new_sigma_b = max(SIGMA_B_MIN, self.sigma_b - SIGMA_B_STEP)
      self.sigma_b = new_sigma_b
    
    # Si le flux est plus haut que le flux stable 
    # on augmente la section efficace des neutrons (sigma_b)
    # en veillant à que sigma_b ne monte pas en dessus de la valeur minimale
    elif (y[2] > STABLE_FLOW):
      new_sigma_b = min(SIGMA_B_MAX, self.sigma_b + SIGMA_B_STEP)
      self.sigma_b = new_sigma_b

    self.sigma_b_set.append(self.sigma_b)

    k1 = self.edo(self, tn, y)
    k2 = self.edo(self, tn + (self.time_step / 2), y + ((self.time_step / 2) * k1))
    k3 = self.edo(self, tn + (self.time_step / 2), y + ((self.time_step / 2) * k2))
    k4 = self.edo(self, tn + self.time_step, y + (self.time_step * k3))
    return (k1 + 2*k2 + 2*k3 + k4)

