#import random, pathlib, os, math, pygame


##test avec mes classes
from All_class.class_dataset import Salles
from All_class.class_voisins_exclus import Voisins_exclus
from All_class.class_optimization_des_sections import Optimization_des_sections

#importation données
test=Salles(app=False)
test.fichiers
info, salle_classe = test.chairs_list_test("Salle Banque Scotia.txt")


###FIXES
# empecher mon algo de changer le fichier data en cours de route (salle classe change)

#tests
salle_classe

# algo olivier
optimize1=Voisins_exclus(salle_classe,1.5,500,methode=1, division=1)
tableau, temps = optimize1.optimize()
optimize1.resultat()
tous_groupes = optimize1.tous_groupes

optimize1.tableau_perfo
optimize1.interruption()
optimize1.graphe_entree()
optimize1.graphe_sortie()
optimize1.temps()

#examiner performance
methode_list=[]
for methode in range(1,5):
    iter_list=[]
    for iteration in range(1):
        optimize1=Voisins_exclus(salle_classe,1.25,1000,methode=methode, division=0)
        tableau, temps = optimize1.optimize()
        nombre_chaises=sum([row[4] for row in tableau])
        tableau_perfo = optimize1.tableau_perfo
        tableau_perfo['iter']=iteration
        tableau_perfo['capacite']=nombre_chaises
        iter_list.append(tableau_perfo)
        
    tableau_concat = pd.concat(iter_list)
    tableau_methode = pd.DataFrame(tableau_concat.groupby('Num_groupe')['Iteration_best','capacite'].mean())
    tableau_methode['methode']=methode
    methode_list.append(tableau_methode)
tableau_comp = pd.concat(methode_list)
print(tableau_comp)


# tableau performance
meta_liste=[]
for methode in range(1,5):
    optimize1=Voisins_exclus(salle_classe,1.5,100,methode=methode, division=1)
    optimize1.optimize()
    tous_groupes = optimize1.tous_groupes
    tous_groupes=[row+[methode] for row in tous_groupes]
    meta_liste.append(tous_groupes)
    
data_graphe = pd.DataFrame(np.concatenate(meta_liste), columns=['groupe', 'iteration','nb_chaises','methode'])

for index, row in data_graphe.iterrows():
    if index==0:
        precedente=row
        pass
    if row['groupe']==precedente['groupe'] and row['methode']==precedente['methode']:
        if row['nb_chaises']<=precedente['nb_chaises']:
            row['nb_chaises']=precedente['nb_chaises']
    precedente=row


import plotly.express as px

# groupes = pd.Categorical(data_graphe[0], categories=[1,2], ordered=True)
methode = pd.Categorical(data_graphe['groupe'], categories=[1,2,3,4], ordered=True)

graphe = px.line(data_graphe, x='iteration',y='nb_chaises', facet_row = 'groupe', color='methode')

# graphe.update_yaxes()
graphe.layout.yaxis2.matches = 'y2'
# graphe.layout.yaxis6.matches = 'y5'
# graphe.layout.yaxis7.matches = 'y5'
# graphe.layout.yaxis8.matches = 'y5'
graphe.show()   
