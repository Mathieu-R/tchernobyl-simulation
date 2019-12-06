# constantes utils pour les équations différentielles #

# constantes de désintégration
LAMBDA_X = 2.0996E-5 # xénon 135
LAMBDA_I = 2.926E-5 # iode 135

# probabilités de production 
# par interaction avec le combustible
GAMMA_X = 0.004  # xénon 135
GAMMA_I = 0.064 # iode 135

# sections efficaces des interactions avec les neutrons
# (probabilité de capture d'un neutron)
SIGMA_X = 2.65E-18 # xénon 135
SIGMA_I = 7E-24 # iode 135

# PHI : Flux de neutrons
PHI = 3e13

# Section efficace macroscopique
# de fission thermique
SIGMA_F = 0.09840 

k = 3
TAU = 1000

# Section efficace des neutrons avec l'Uranium
SIGMA_U = 0.1355

# section efficace des neutrons
# avec barres de ralentissement
SIGMA_B_MIN = 0.1
SIGMA_B_MAX = 0.2

# "vitesse" des barres de ralentissement
SIGMA_B_STEP = 0.0001

# Flux de départ
FLOW_START = 1E10

# Flux stable
STABLE_FLOW = 1E15

# Drop du flux à 1% de sa valeur stable
FLOW_DROP = STABLE_FLOW / 100