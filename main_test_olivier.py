from All_class.class_dataset import Dataset
from All_class.class_optimization_random import Optimization_random
from All_class.class_application import Application
import random, pathlib, os, math, pygame
from sys import exit

    
### Assigner la class Dataset à la variable "data"     
data = Dataset()
### Print le résultat de la fonction list_files() de la classe Dataset
print(data.list_files())
### Assigner à le résultat de la fonction data_selection_list() de la classe Dataset à la variable "data_selection" 
data_selection = data.chairs_list("salle_test54.txt")
for chair in data_selection:
    print(chair)
### Assigner à le résultat de la fonction room_info() de la classe Dataset à la variable "room_info"   
room_info = data.room_info("salle_test54_info.txt")
print(room_info)

### Assigner la classe Optimization_random à la variable "optimization"
optimization = Optimization_random(data_selection)
### Assigner à le résultat de la fonction optimize() de la classe Optimization_random à la variable "optimization_export"
### Choix de la valeur 25 pour le paramètre optionel "rate_use"
optimization_export = optimization.optimize(25)
for chair in optimization_export:
    print(chair)

app = Application(optimization_export, room_info)
app.game_loop()