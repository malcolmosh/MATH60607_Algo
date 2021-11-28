#import random, pathlib, os, math, pygame
import pandas as pd
import numpy as np
import plotly.express as px


##test avec mes classes
from All_class.class_dataset import Salles
from All_class.class_voisins_exclus import Voisins_exclus
from All_class.class_optimization_des_sections import Optimization_des_sections

#importation données
test=Salles(app=False)
test.fichiers
info, salle_classe = test.chairs_list_test("Salle Cogeco.txt")


#tests
salle_classe

# algo olivier
optimize1=Voisins_exclus(salle_classe,1.5,100,methode=1, division=1)
tableau, temps = optimize1.optimize()
optimize1.resultat()
tous_groupes = optimize1.tous_groupes

optimize1.tableau_perfo
optimize1.interruption()
optimize1.graphe_entree()
optimize1.graphe_sortie()
optimize1.temps()

#examiner performance
# methode_list=[]
# for i, value in enumerate(["Voisin aléatoire","Plus proche voisin","Plus loin voisin","Plus proche voisin pondéré"]):
#     iter_list=[]
#     for epoch in range(1):
#         optimize1=Voisins_exclus(salle_classe,1.25,100,methode=i+1, division=1)
#         tableau, temps = optimize1.optimize()
#         nombre_chaises=sum([row[4] for row in tableau])
#         tableau_perfo = optimize1.tableau_perfo
#         tableau_perfo['iter']=epoch
#         tableau_perfo['capacite']=nombre_chaises
#         iter_list.append(tableau_perfo)
        
#     tableau_concat = pd.concat(iter_list)
#     tableau_methode = pd.DataFrame(tableau_concat.groupby('Num_groupe')[['Iteration_best','capacite']].mean())
#     tableau_methode['methode']=value
#     methode_list.append(tableau_methode)
    
# tableau_comp = pd.concat(methode_list)
# print(tableau_comp)


#creer salle classe grand carré (500 places)
test=[]

for i in range(1,20):
    for j in range(1,10):
        a=[i,"south",i,j,False]
        test.append(a)

for i in range(1,len(salle_classe)):
    test[i][0]=i+1
salle_classe=test

# tableau performance
meta_liste=[]
for i in range(1,5):
    optimize1=Voisins_exclus(salle_classe,2,100,methode=i, division=1)
    optimize1.optimize()
    tous_groupes = optimize1.tous_groupes
    #tous_groupes=[row for row in tous_groupes]
    meta_liste.append(tous_groupes)
    
   
data_graphe = pd.DataFrame(np.concatenate(meta_liste), columns=['groupe', 'iteration','nb_chaises','methode_num'])
data_graphe['methode'] = data_graphe['methode_num'].map({1:"Voisin aléatoire",2:"Plus proche voisin",3:"Plus loin voisin",4:"Plus proche voisin pondéré"}) 


#remplacer le nombre de chaises dans chaque méthode par le maximum, une fois qu'il est atteint
for i in range(1, len(data_graphe)):
    if data_graphe.loc[i,'groupe']==data_graphe.loc[i-1,'groupe'] and data_graphe.loc[i,'methode_num']==data_graphe.loc[i-1,'methode_num']:
        if data_graphe.loc[i,'nb_chaises']<=data_graphe.loc[i-1,'nb_chaises']:
            data_graphe.loc[i,'nb_chaises']=data_graphe.loc[i-1,'nb_chaises']
     
# #enlever groupes avec 1 chaise
# data_graphe.drop(data_graphe[data_graphe["nb_chaises"]==1].index, inplace=True)
# data_graphe.reset_index(inplace=True)

#offset values by methode
for i in range(1, len(data_graphe)):
    if data_graphe.loc[i,'methode_num']==2:
        data_graphe.loc[i,'nb_chaises']+=0.05
    elif data_graphe.loc[i,'methode_num']==3:
        data_graphe.loc[i,'nb_chaises']+=0.10
    elif data_graphe.loc[i,'methode_num']==4:
        data_graphe.loc[i,'nb_chaises']+=0.15     

#graphe 1
graphe = px.line(data_graphe, x='iteration',y='nb_chaises', facet_row = 'groupe', color='methode')
graphe.update_yaxes()
#graphe.layout.yaxis2.matches = 'y2'
graphe.show()   


#graphe 2
graphe = px.line(data_graphe, x='iteration',y='nb_chaises', facet_row = 'groupe', facet_col="methode", color='methode')
# graphe.update_yaxes()
graphe.layout.yaxis2.matches = 'y2'
graphe.layout.yaxis6.matches = 'y5'
graphe.layout.yaxis7.matches = 'y5'
graphe.layout.yaxis8.matches = 'y5'
graphe.show()   


#tester avec manuvie, avec grande salle rectangulaire, avec grande salle qui a des division