import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import tkinter as tk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandas import DataFrame
from edo_solver.neutrons_flow import NeutronsFlow
from edo_solver.edo import neutrons_flow_edo
from utils import day_to_seconds
from constants import FLOW_START, TIME_INTERVAL


class GraphicInterface():
  def __init__(self):
    # fenêtre principale
    self._main_window = tk.Tk()
    # Indique si la simulation est lancée
    self._started = False
    self._paused = False

    self.gui()

  # lancement de l'interface graphique
  def gui(self):
    field_label = tk.Label(
      self._main_window, 
      text="Quantité de flux, Iode et Xenon en fonction du temps:",
      font=("Helvetica", 15)
    )

    field_label.pack()

    bouton_flux = tk.Button(self._main_window, text="Flux de neutrons", command=plot_neutrons_flow)
    bouton_flux.pack()
    
    bouton_flux_commandes = tk.Button(self._main_window, text="Barres de contrôle", command=control_bars)
    bouton_flux_commandes.pack()

    self._main_window.mainloop()

  def plot_neutrons_flow(self):
    # Lancement de la simulation
    if not self._started:
      compute_neutrons_flow(
        xenon_start=0,
        stop=day_to_seconds(20),
        title="Flux de neutrons - stabilisation"
      )
        
    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)

    def animate(step):
      xs=[]
      ys=[]

      for t_h in range(step):
        if not pause:
          t_s = t_h/3600
          xs.append(t_h)
          ys.append((2+7*t_s+20*t_s**2)/(1+t_s**2))

      if len(xs)>24:
        xs = xs[-24:]
        ys = ys[-24:]

      ax1.clear()
      ax1.plot(xs, ys)

      plt.xlabel('Temps en h')
      plt.ylabel('Flux de neutron en n cm**-2 s**-1')
      plt.title('Flux de neutron en fonction du temps')	

      
    ani = animation.FuncAnimation(fig, animate, interval=1000) 
    plt.show()

  def control_bars(self):
    graphe_flux_commandes = tk.Toplevel(self.main_window)
    titre_flux_commandes = tk.Label(graphe_flux_commandes, text="Commandes pour le graphe du flux de neutron",font=("Helvetica", 15))
    titre_flux_commandes.pack()
    titre_scale = tk.Label(graphe_flux_commandes, text="Choisir valeur des barres de ralentissement")
    titre_scale.pack()
    var = tk.DoubleVar()
    scale = tk.Scale(graphe_flux_commandes, variable=var, from_=0.2, to=0.1, resolution = 0.0001, length=200)
    scale.pack()
    pause = False
    def onClick():
          global pause
          pause = True
    bouton_interupteur = tk.Button(graphe_flux_commandes, text="Arrêter la simulation" , command=onClick)
    bouton_interupteur.pack()

  def compute_neutrons_flow (self, xenon_start, stop, title):
      # default values
    T0 = 0
    STOP = stop
    FLOW_CI = [1.0, xenon_start, FLOW_START] # [I(T_0), X(T_0), PHI[T_0]]

    title = title
    x_label = "temps (h)"
    y_label = "Abondance / Flux"
    legends = ['Iode', 'Xénon', 'Flux de neutrons']

    isotope_abundance_rk4 = NeutronsFlow(title, y_label, x_label, legends, neutrons_flow_edo, T0, FLOW_CI, TIME_INTERVAL, STOP)
    isotope_abundance_rk4.resolve()