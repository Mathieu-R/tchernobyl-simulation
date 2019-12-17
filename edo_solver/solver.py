import matplotlib.pyplot as plt
import numpy as np

from utils import seconds_to_hour

class EDONumericalResolution:
  def __init__(self, edo, ci, full_time_range, time_step):
    """
    @edo: fonction qui retourne [y' = CI, y'' = EDO] sous forme de matrice
    @ci : liste des conditions initiales
    @full_time_range : ndarray contenant [time_start -> time_end] pour chaque time_step
    @time_step : intervalle de temps
    """
    # function that return [y' = CI, y'' = EDO] as a matrix
    self.edo = edo
    self.ci = ci
    self.full_time_range = full_time_range
    self.time_step = time_step

    # keep track of data
    #self._time_set = np.zeros([len(full_time_range)])
    self.y_set = np.zeros([len(full_time_range), len(ci)])

  def resolve(self, sub_interval = None):
    raise NotImplemented

  def graph(self, title, edo_legends, x_label, y_label):
    full_time_range_in_hours = map(lambda t: seconds_to_hour(t), self.full_time_range)
    plt.plot(self.full_time_range_in_hours, self.y_set)
    plt.title(title)
    # https://stackoverflow.com/questions/44632571/pyplot-legend-only-displaying-one-letter?noredirect=1&lq=1
    plt.legend(edo_legends, loc="upper right")
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.yscale('log')
    plt.show()

  def graph_sigma_b(self):
    plt.plot(self.full_time_range, np.array(self.sigma_b_set))
    plt.title("Barres de contrôle")
    # https://stackoverflow.com/questions/44632571/pyplot-legend-only-displaying-one-letter?noredirect=1&lq=1
    plt.legend(["Section efficace des neutrons avec les barres de contrôle"], loc="upper right")
    plt.xlabel(self.x_label)
    plt.ylabel("Sigma B")
    plt.show()