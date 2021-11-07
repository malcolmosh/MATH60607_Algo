from All_class.class_dataset import Salles
from All_class.class_optimization_random import Optimization_random
from All_class.class_optimization_des_sections import Optimization_des_sections
import random, pathlib, os, math
import pandas as pd
from sys import exit

#appeler la méthode pour aller chercher les données
data_method = Salles(folder_data='Data',app=False)
info, data = data_method.chairs_list_test("Salle Saine Marketing.txt")

print(data)
print("----------------------")

opti = Optimization_des_sections(data, 4)
data_optimize, opti_time = opti.optimize()

print(f"Le temps total est de {round(opti_time,2)} secondes")
print(data_optimize)