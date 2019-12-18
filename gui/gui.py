import numpy as np
import tkinter as tk
from ttkthemes import themed_tk
from tkinter import ttk

from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk

from edo_solver.edo import neutrons_flow_edo 
from edo_solver.neutrons_flow import NeutronsFlow
from edo_solver.plot_animation import PlotAnimation
from utils import day_to_seconds, hour_to_seconds
from constants import FLOW_START, TIME_INTERVAL, TEXT_FONT

class GraphicInterface():
  def __init__(self):
    self.root = themed_tk.ThemedTk()
    self.root.minsize(800, 600)
    self.root.title("Simulation du réacteur d'une centrale nucléaire") 
    self.root.rowconfigure(0, weight=1)
    self.root.columnconfigure(0, weight=1)

    main_frame = ttk.Frame(self.root)
    main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    main_frame.rowconfigure(0, weight=1)
    main_frame.columnconfigure(0, weight=1)

    # contain notebook
    notebook_frame = ttk.Frame(main_frame, borderwidth=8)
    notebook_frame.grid(row=0, column=0, sticky="nsew")
    notebook_frame.rowconfigure(0, weight=1)
    notebook_frame.columnconfigure(0, weight=1)

    # contains plots
    notebook = ttk.Notebook(notebook_frame)
    notebook.grid(row=0, column=0, sticky="nsew")
    notebook.rowconfigure(0, weight=1)

    # contain neutron flow plot + onglet
    neutrons_flow_frame = ttk.Frame(notebook)
    notebook.add(neutrons_flow_frame, text="Flux de neutrons")

    # instance plot class
    self.neutrons_flow_plot = PlotAnimation(tk_root=neutrons_flow_frame)

    toolbar1 = NavigationToolbar2Tk(self.neutrons_flow_plot, neutrons_flow_frame)
    toolbar1.update()

    parameters_frame = ttk.LabelFrame(main_frame, text="Paramètres")
    parameters_frame.grid(row=0, column=1, sticky="nsew")
    parameters_frame.rowconfigure(0, weight=1)
    parameters_frame.rowconfigure(1, weight=5)
    parameters_frame.rowconfigure(2, weight=5)
    parameters_frame.rowconfigure(3, weight=5)
    parameters_frame.rowconfigure(4, weight=5)
    parameters_frame.rowconfigure(5, weight=5)
    parameters_frame.columnconfigure(0, weight=1)

    self.field_I0 = tk.StringVar(value="1.0")
    self.field_X0 = tk.StringVar(value="2e15")
    self.field_flow0 = tk.StringVar(value=f"{FLOW_START}")
    self.field_time_interval = tk.StringVar(value="10")
    self.field_stop = tk.StringVar(value="100")

    label_I0 = ttk.Label(parameters_frame, text="Iode initial")
    entry_I0 = ttk.Entry(parameters_frame, textvariable=self.field_I0)

    label_X0 = ttk.Label(parameters_frame, text="Xénon initial")
    entry_X0 = ttk.Entry(parameters_frame, textvariable=self.field_X0)

    label_flow0 = ttk.Label(parameters_frame, text="Flux initial")
    entry_flow0 = ttk.Entry(parameters_frame, textvariable=self.field_flow0)

    label_time_interval = ttk.Label(parameters_frame, text="Pas de temps (s)")
    entry_time_interval = ttk.Entry(parameters_frame, textvariable=self.field_time_interval)

    label_stop = ttk.Label(parameters_frame, text="Durée de la simulation (h)")
    entry_stop = ttk.Entry(parameters_frame, textvariable=self.field_stop)

    label_I0.grid(row=1, column=0, sticky='new')
    label_X0.grid(row=1, column=0, sticky='ew')
    label_flow0.grid(row=1, column=0, sticky='sew')
    
    label_time_interval.grid(row=2, column=0, sticky='new')
    label_stop.grid(row=2, column=0, sticky='ew')
    
    entry_I0.grid(row=1, column=1, sticky='new')
    entry_X0.grid(row=1, column=1, sticky='ew')
    entry_flow0.grid(row=1, column=1, sticky='sew')

    entry_time_interval.grid(row=2, column=1, sticky='new')
    entry_stop.grid(row=2, column=1, sticky='ew')

    launch_simulation_button = ttk.Button(parameters_frame, text="Lancer la simulation", command=self.plot_neutrons_flow)
    launch_simulation_button.grid(row=4, column=0, columnspan=2, sticky="new")
    
    manage_control_bars_button = ttk.Button(parameters_frame, text="Gérer les barres de contrôle", command=self.control_bars)
    manage_control_bars_button.grid(row=4, column=0, columnspan=2, sticky="ew")

    quit_button = ttk.Button(parameters_frame, text="Quitter", command=self.quit)
    quit_button.grid(row=4, column=0, columnspan=2, sticky="sew")

    # redimensionnement des boutons, textes
    for child in parameters_frame.winfo_children():
      if isinstance(child, ttk.Label):
        child.config(font=TEXT_FONT)
      child.grid_configure(padx=5, pady=5)

    # Indique si la simulation est lancée
    self.started = False

    # edo simulation
    self.simulation = None
    
    self.root.mainloop()

  def plot_neutrons_flow(self):
    # Lancement de la simulation
    if not self.started: 
      self.started = True
      I0 = float(self.field_I0.get())
      X0 = float(self.field_X0.get())
      flow0 = float(self.field_flow0.get())
      time_step = float(self.field_time_interval.get())
      time_end = hour_to_seconds(int(self.field_stop.get()))

      # incrémente car la dernière valeur n'est pas prise en compte
      full_time_range = np.arange(0, time_end + time_step, time_step)

      FLOW_CI = [I0, X0, flow0] # [I(T_0), X(T_0), PHI[T_0]]

      self.simulation = NeutronsFlow(
        edo=neutrons_flow_edo, 
        ci=FLOW_CI,
        full_time_range=full_time_range,
        time_step=time_step
      )

      self.neutrons_flow_plot.animate(self.simulation, time_end)

  def on_stop_simulation_button_click (self):
    self.paused = True

  def control_bars(self):
    command_window = ttk.Toplevel(self.root)
    
    scale = ttk.Scale(self.command_window, var=ttk.DoubleVar(), from_=0.2, to_=0.1, resolution=0.001, length=200, command=self.update_bars)
    scale.grid()

    flow_control_bars = tk.Toplevel(self.root)

  def update_bars(self, sigma_b):
    self.simulation.sigma_b = sigma_b

  def quit(self):
    self.root.quit()
    self.root.destroy()