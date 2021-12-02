#import random, pathlib, os, math, pygame
import pandas as pd
import numpy as np
import plotly.express as px


##test avec mes classes
from All_class.class_dataset import Salles
from All_class.class_voisins_exclus import Voisins_exclus
from All_class.class_grow import Grow

#importation données
test=Salles(app=False)
test.fichiers
salle_1="Salle Mega 1105.txt"
salle_2 = "Salle Banque Scotia.txt"
salle_3 = "Salle Cogeco.txt"
salle_4 = "Salle Manuvie.txt"
salle_5 = "Salle Saine Marketing.txt"
info, salle_classe = test.chairs_list_test(salle_5)

print(info)
print(salle_classe)

opti = Grow(salle_classe, 2, 1000) #division

chairs = opti.optimize()

print(chairs)