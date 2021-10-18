from All_class.class_dataset import Dataset
from All_class.class_optimization_random import Optimization_random
import pygame

#Assigner la class Dataset à la variable "data"     
data = Dataset()
#Print le résultat de la fonction list_files() de la classe Dataset
print(data.list_files())
#Assigner à le résultat de la fonction data_selection_list() de la classe Dataset à la variable "data_selection" 
data_selection = data.data_selection_list("salle_test50.txt")
for chair in data_selection:
    print(chair)

#Assigner la classe Optimization_random à la variable "optimization"
optimization = Optimization_random(data_selection)
#Assigner à le résultat de la fonction optimize() de la classe Optimization_random à la variable "optimization_export"
#Choix de la valeur 25 pour le paramètre optionel "rate_use"
optimization_export = optimization.optimize(25)
for chair in optimization_export:
    print(chair)