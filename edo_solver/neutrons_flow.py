from .rk4 import RK4Method
from constants import SIGMA_B_MIN, SIGMA_B_MAX, SIGMA_B_STEP, STABLE_FLOW, FLOW_DROP
from utils import seconds_to_hour

class NeutronsFlow(RK4Method):
  def __init__(self, title, y_label, x_label, edo_legends, edo, t0, ci, time_interval, stop):
    self._sigma_b = SIGMA_B_MIN
    self._timer_started = False
    self._timer_start = 0
    self._sigma_b_set = [SIGMA_B_MIN]
    super().__init__(title, y_label, x_label, edo_legends, edo, t0, ci, time_interval, stop)

  def derivatives(self, tn, y):
    # Si le flux est plus ou moins stabilisé
    # On démarre un timer et on attend 24 heures
    # Après cela, on baisse le flux à 1% de sa valeur stable
    if (y[2] > STABLE_FLOW - 0.5E10 and y[2] < STABLE_FLOW + 0.5E10 and not self._timer_started):
      self._timer_started = True
      self._timer_start = tn

    if (self._timer_started and seconds_to_hour(tn - self._timer_start) >= 24):
      # Si le flux est plus bas que le flux stable
      # et que sigma_b ne descend pas en dessous de la valeur minimale
      # on diminue la section efficace des neutrons (sigma_b)
      if (y[2] < FLOW_DROP and self._sigma_b > SIGMA_B_MIN):
        self._sigma_b -= SIGMA_B_STEP
      
      # Si le flux est plus haut que le flux stable 
      # et que sigma_b ne dépasse pas sa valeur maximale
      # on diminue la section efficace des neutrons (sigma_b)
      elif (y[2] > FLOW_DROP and self._sigma_b < SIGMA_B_MAX):
        self._sigma_b += SIGMA_B_STEP

    #if (y[2] > STABLE_FLOW - (1E10 / 1000)

    # Si le flux est plus bas que le flux stable
    # et que sigma_b ne descend pas en dessous de la valeur minimale
    # on diminue la section efficace des neutrons (sigma_b)
    if (y[2] < STABLE_FLOW and self._sigma_b > SIGMA_B_MIN):
      self._sigma_b -= SIGMA_B_STEP
    
    # Si le flux est plus haut que le flux stable 
    # et que sigma_b ne dépasse pas sa valeur maximale
    # on diminue la section efficace des neutrons (sigma_b)
    elif (y[2] > STABLE_FLOW and self._sigma_b < SIGMA_B_MAX):
      self._sigma_b += SIGMA_B_STEP

    self._sigma_b_set.append(self._sigma_b)

    k1 = self._edo(self, tn, y)
    k2 = self._edo(self, tn + (self._time_interval / 2), y + ((self._time_interval / 2) * k1))
    k3 = self._edo(self, tn + (self._time_interval / 2), y + ((self._time_interval / 2) * k2))
    k4 = self._edo(self, tn + self._time_interval, y + (self._time_interval * k3))
    return (k1 + 2*k2 + 2*k3 + k4)

