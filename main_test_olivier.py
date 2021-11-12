#import random, pathlib, os, math, pygame


##test avec mes classes
from All_class.class_dataset import Salles
from All_class.class_voisins_exclus_backup import Voisins_exclus
from All_class.class_optimization_des_sections import Optimization_des_sections

#importation données
test=Salles(app=False)
test.fichiers
info, salle_classe = test.chairs_list_test("Salle Saine Marketing - 1x1metre dist.txt")


#tests
salle_classe

# algo olivier
optimize1=Voisins_exclus(salle_classe,2,5000,methode=1, division=1, maximum_time=0.05)
tableau, temps = optimize1.optimize()
optimize1.resultat()
optimize1.interruption()
#optimize1.graphe_entree()
optimize1.graphe_sortie()
optimize1.temps()

# algo mahnaz 
optimize2 = Optimization_des_sections(salle_classe,2)
sortie, temps = optimize2.optimize()

## ajouter
#résultat
sum([chaise[4] for chaise in sortie])

# suppress warnings for panda slices
# retirer les merge ?
