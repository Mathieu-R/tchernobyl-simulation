## tchernobyl-simulation

Projet de méthodes numériques visant à simuler le réacteur d'une centrale nucléaire ainsi que la catastrophe de Tchernobyl.    

Plus d'infos : https://cp3-git.irmp.ucl.ac.be/mdelcourt/lphys1201/wikis/projet-Tchernobyl

### utilisation
```
$ chmod +x setup.sh start.sh
$ ./setup.sh
$ ./start.sh
```

### captures

> Simulation du flux de neutrons avec explosion de la centrale.
> Drop du flux à 1% de sa valeur stable 24h après la stabilisation du flux de neutrons
![simulation du flux de neutrons](/figures/neutron_flow_with_central_explosion.png?raw=true)

> Mouvement des barres de contrôles lors de la simulation précédente
![barres de contrôle](/figures/control_bars_movement.png?raw=true)

### troubleshooting
En cas de difficulté avec l'installation des packages, il peut être utile d'aliaser pip 
```
$ sudo vim ~/.bashrc # où .zshrc
# ajouter alias pip=pip3 à la fin de ce fichier
# ajouter eval "$(pyenv init -)" à la fin de ce fichier
$ source ~/.zshrc 
```