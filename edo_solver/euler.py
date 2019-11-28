import matplotlib.pyplot as plt
import numpy as np
from random import randint

# Méthode d'Euler
class EulerMethod(EDONumericalResolution):
  def resolve(self):
    y = list(self._ci) # [y(t0), y'(t0)]

    # range function for float
    for t in np.arange(self._t0, self._stop, self._time_interval):
      # update system of edo for the point we're in
      system = self._edo(t, y)
      # matrix multiplication by a scalar
      y += self._time_interval * system

      self._time_set.append(t)
      # [:] allow that modifying y do not modify y_set because of references
      # for numpy array, use copy() method
      self._y_set.append(y.copy())
    
    # matrix transposition
    self._y_set = np.array(self._y_set).transpose()