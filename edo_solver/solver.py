import matplotlib.pyplot as plt

class EDONumericalResolution:
  def __init__(self, title, y_label, x_label, edo_legends, edo, t0, ci, time_interval, stop, modify_flow = False, day_of_flow_modification = None, next_flow = None):
    # function that return [y' = CI, y'' = EDO] as a matrix
    self._edo = edo
    self._t0 = t0
    # [y(0), y'(0)]
    self._ci = ci
    self._time_interval = time_interval
    self._stop = stop

    # modify flow
    self._modify_flow = modify_flow
    self._day_of_flow_modification = day_of_flow_modification
    self._next_flow = next_flow

    # keep track of data
    self._time_set = []
    self._y_set = []

    # graph
    self._title = title
    self._x_label = x_label
    self._y_label = y_label
    self._edo_legends = edo_legends

  def resolve(self):
    raise NotImplemented

  def graph(self): 
    plt.plot(self._time_set, self._y_set)
    plt.title(self._title)
    # https://stackoverflow.com/questions/44632571/pyplot-legend-only-displaying-one-letter?noredirect=1&lq=1
    plt.legend(self._edo_legends, loc="upper right")
    plt.xlabel(self._x_label)
    plt.ylabel(self._y_label)
    plt.yscale('log')
    #plt.grid(True,which="both").
    plt.show()