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
    root = themed_tk.ThemedTk()
    root.minsize(800, 600)
    root.title("Simulation du réacteur d'une centrale nucléaire") 
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    main_frame = ttk.Frame(root)
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
    neutrons_flow_plot = PlotAnimation(tk_root=neutron_flow_frame)

    print(neutrons_flow_frame)
    toolbar1 = NavigationToolbar2Tk(neutrons_flow_plot, neutrons_flow_frame)
    toolbar1.update()

    self._parameters_frame = ttk.LabelFrame(self._main_frame, text="Paramètres")
    self._parameters_frame.grid(row=0, column=1, sticky="nsew")
    self._parameters_frame.rowconfigure(0, weight=1)
    self._parameters_frame.rowconfigure(1, weight=5)
    self._parameters_frame.rowconfigure(2, weight=5)
    self._parameters_frame.rowconfigure(3, weight=5)
    self._parameters_frame.rowconfigure(4, weight=5)
    self._parameters_frame.rowconfigure(5, weight=5)
    self._parameters_frame.columnconfigure(0, weight=1)

    self._field_I0 = tk.StringVar(value="1.0")
    self._field_X0 = tk.StringVar(value="2e15")
    self._field_flow0 = tk.StringVar(value=f"{FLOW_START}")
    self._field_time_interval = tk.StringVar(value="10")
    self._field_stop = tk.StringVar(value="100")

    self._label_I0 = ttk.Label(self._parameters_frame, text="Iode initial")
    self._entry_I0 = ttk.Entry(self._parameters_frame, textvariable=self._field_I0)

    self._label_X0 = ttk.Label(self._parameters_frame, text="Xénon initial")
    self._entry_X0 = ttk.Entry(self._parameters_frame, textvariable=self._field_X0)

    self._label_flow0 = ttk.Label(self._parameters_frame, text="Flux initial")
    self._entry_flow0 = ttk.Entry(self._parameters_frame, textvariable=self._field_flow0)

    self._label_time_interval = ttk.Label(self._parameters_frame, text="Pas de temps (s)")
    self._entry_time_interval = ttk.Entry(self._parameters_frame, textvariable=self._field_time_interval)

    self._label_stop = ttk.Label(self._parameters_frame, text="Durée de la simulation (h)")
    self._entry_stop = ttk.Entry(self._parameters_frame, textvariable=self._field_stop)

    self._label_I0.grid(row=1, column=0, sticky='new')
    self._label_X0.grid(row=1, column=0, sticky='ew')
    self._label_flow0.grid(row=1, column=0, sticky='sew')
    
    self._label_time_interval.grid(row=2, column=0, sticky='new')
    self._label_stop.grid(row=2, column=0, sticky='ew')
    
    self._entry_I0.grid(row=1, column=1, sticky='new')
    self._entry_X0.grid(row=1, column=1, sticky='ew')
    self._entry_flow0.grid(row=1, column=1, sticky='sew')

    self._entry_time_interval.grid(row=2, column=1, sticky='new')
    self._entry_stop.grid(row=2, column=1, sticky='ew')

    launch_simulation_button = ttk.Button(self._parameters_frame, text="Lancer la simulation", command=self.plot_neutrons_flow)
    launch_simulation_button.grid(row=4, column=0, columnspan=2, sticky="new")
    
    manage_control_bars_button = ttk.Button(self._parameters_frame, text="Gérer les barres de contrôle", command=self.control_bars)
    manage_control_bars_button.grid(row=4, column=0, columnspan=2, sticky="ew")

    quit_button = ttk.Button(self._parameters_frame, text="Quitter", command=self.quit)
    quit_button.grid(row=4, column=0, columnspan=2, sticky="sew")

    # redimensionnement des boutons, textes
    for child in self._parameters_frame.winfo_children():
      if isinstance(child, ttk.Label):
        child.config(font=TEXT_FONT)
      child.grid_configure(padx=5, pady=5)

    # Indique si la simulation est lancée
    self._started = False

    # edo simulation
    self._simulation = None
    
    self._root.mainloop()

  def plot_neutrons_flow(self):
    # Lancement de la simulation
    if not self._started: 
      I0 = float(self._field_I0.get())
      X0 = float(self._field_X0.get())
      flow0 = float(self._field_flow0.get())
      time_interval = float(self._field_time_interval.get())
      stop = int(self._field_stop.get())

      FLOW_CI = [I0, X0, flow0] # [I(T_0), X(T_0), PHI[T_0]]

      self._simulation = NeutronsFlow(
        edo=neutrons_flow_edo, 
        t0=0,
        ci=FLOW_CI,
        time_interval=time_interval,
        stop=hour_to_seconds(stop)
      )

      # animation = PlotAnimation(
      #   time_interval=time_interval, 
      #   time_refresh=3600, 
      #   ci=FLOW_CI, 
      #   simulation_time=hour_to_seconds(stop),
      #   simulation=self._simulation,
      # )
      animation.animate(self._simulation)
      self._started = True

  def on_stop_simulation_button_click (self):
    self._paused = True

  def control_bars(self):
    flow_control_bars = tk.Toplevel(self._root)

    title = tk.Label(
      flow_control_bars, 
      text="Commandes pour le graphe du flux de neutron",
      font=("Helvetica", 15)
    )
    title.grid()

    subtitle = tk.Label(flow_control_bars, text="Valeur des barres de ralentissement")
    subtitle.grid()

    scale = tk.Scale(
      flow_control_bars, 
      variable=var, 
      from_=0.2, 
      to=0.1, 
      resolution = 0.0001, 
      length=200,
      command=self.update_bars
    )
    scale.grid()

  def update_bars(self, sigma_b):
    self._simulation.set_sigma_b(sigma_b)

  def quit(self):
    self._root.quit()
    self._root.destroy()

