from All_class.class_optimization_random import Optimization_random
from All_class.class_application import Application
#import random, pathlib, os, math, pygame
from sys import exit


##test avec mes classes
from All_class.class_dataset import Salles
from All_class.class_voisins_exclus import Voisins_exclus

test=Salles(app=False)

test.fichiers

info, salle_classe = test.chairs_list_test("Salle Saine Marketing - 1x1metre dist.txt")


optimize1=Voisins_exclus(salle_classe,2,1000,methode=1)
optimize1.optimize()
optimize1.resultat()
optimize1.interruption()
optimize1.graphe_entree()
#optimize1.graphe_sortie()
optimize1.temps()



#optimize1.tableau()
#sortie = optimize1.tableau()

##tests

