#import random, pathlib, os, math, pygame
import pandas as pd
import numpy as np
import plotly.express as px


##test avec mes classes
from All_class.class_dataset import Salles
from All_class.class_voisins_exclus import Voisins_exclus

#importation données
test=Salles(app=False)
test.fichiers
salle_1="Salle Mega 1105.txt"
salle_2 = "Salle Banque Scotia.txt"
salle_3 = "Salle Cogeco.txt"
salle_4 = "Salle Manuvie.txt"
salle_5 = "Salle Saine Marketing.txt"
info, salle_classe = test.chairs_list_test(salle_1)

#tests
salle_classe

# algo olivier
optimize1=Voisins_exclus(salle_classe,distance=2, iterations=500, methode=3, division=1)
tableau, temps = optimize1.optimize()
optimize1.resultat()
optimize1.graphe_sortie()
# tous_groupes = optimize1.tous_groupes

# optimize1.tableau_perfo
# optimize1.interruption()
# optimize1.graphe_entree()

# optimize1.temps()



meta_liste_2=[]
for epoch in range(1,11):
    meta_liste=[]
    for i in range(1,5):
        optimize1=Voisins_exclus(salle_classe,2,100,methode=i, division=1)
        optimize1.optimize()
        tous_groupes = [[epoch]+row for row in optimize1.tous_groupes]
        #tous_groupes=[row for row in tous_groupes]
        meta_liste.append(tous_groupes)
    meta_liste_2.append(meta_liste)


#créer dataframe
data_graphe = pd.DataFrame(np.concatenate(np.concatenate(meta_liste_2)),columns=['epoch', 'groupe', 'iteration','nb_chaises','methode_num'])
data_graphe= data_graphe.groupby(['methode_num','groupe','iteration'],as_index=False).mean()
data_graphe = data_graphe.drop(columns="epoch")
#data_graphe = pd.DataFrame(np.concatenate(meta_liste), columns=['groupe', 'iteration','nb_chaises','methode_num'])
data_graphe['methode'] = data_graphe['methode_num'].map({1:"Voisin aléatoire",2:"Plus proche voisin",3:"Plus loin voisin",4:"Plus proche voisin pondéré"}) 
data_graphe.reset_index(inplace=True)

#écraser les groupes
# on additionne les chaises au travers de tous les groupes, pour chaque itération et pour chaque méthode
data_graphe = data_graphe.groupby(["methode_num", "methode", "iteration"], as_index=False).sum()

# # #remplacer le nombre de chaises dans chaque méthode et dans chaque groupe par le maximum, une fois qu'il est atteint
# for i in range(1, len(data_graphe)):
#     if data_graphe.loc[i,'groupe']==data_graphe.loc[i-1,'groupe'] and data_graphe.loc[i,'methode_num']==data_graphe.loc[i-1,'methode_num']:
#         if data_graphe.loc[i,'nb_chaises']<=data_graphe.loc[i-1,'nb_chaises']:
#             data_graphe.loc[i,'nb_chaises']=data_graphe.loc[i-1,'nb_chaises']
     
# #convertir en pourcentage
max_chaises_atteint = data_graphe['nb_chaises'].max()
# data_graphe['nb_chaises']=(data_graphe['nb_chaises']/max_chaises_atteint)*100
  
#trouver l'itération maximale à laquelle une des méthodes finit par converger à 100% (pour ajuster axes)
derniere_iter_max = data_graphe[data_graphe['nb_chaises']==max_chaises_atteint].groupby("methode_num").first()['iteration'].max()

# # # #offset values by methode
# for i in range(1, len(data_graphe)):
#     if data_graphe.loc[i,'methode_num']==2:
#         data_graphe.loc[i,'nb_chaises']+=0.01
#     elif data_graphe.loc[i,'methode_num']==3:
#         data_graphe.loc[i,'nb_chaises']-=0.01
#     elif data_graphe.loc[i,'methode_num']==4:
#         data_graphe.loc[i,'nb_chaises']+=0.02

#produire graphe
graphe = px.line(data_graphe, x='iteration',y='nb_chaises', color="methode", 
                 labels=dict(iteration="Itération", nb_chaises="Capacité calculée", methode="Méthode"), 
                 title="Grande salle (1105 sièges), avec division")
graphe.update_traces(mode="lines", line_shape="vh", line=dict(width=4))
graphe.add_hline(y=max_chaises_atteint, line_dash="dot", annotation_text="Max. atteint :"+str(round(max_chaises_atteint,2))+" chaises", annotation_position="top left", 
                 line_color="red")
graphe.update_xaxes(range=[0,100])
graphe.show(config=config)   

config = {
  'toImageButtonOptions': {
    'format': 'png', # one of png, svg, jpeg, webp
    'filename': 'plot',
    'scale': 5 # Multiply title/legend/axis/canvas sizes by this factor
  }
}


# # #offset values by methode
# for i in range(1, len(data_graphe)):
#     if data_graphe.loc[i,'methode_num']==2:
#         data_graphe.loc[i,'nb_chaises']+=0.05
#     elif data_graphe.loc[i,'methode_num']==3:
#         data_graphe.loc[i,'nb_chaises']+=0.10
#     elif data_graphe.loc[i,'methode_num']==4:
#         data_graphe.loc[i,'nb_chaises']+=0.15   


#graphe.update_yaxes()
#graphe.layout.yaxis2.matches = 'y2'


# #enlever groupes avec 1 chaise
# data_graphe.drop(data_graphe[data_graphe["nb_chaises"]==1].index, inplace=True)
# data_graphe.reset_index(inplace=True)

# #offset values by methode
# for i in range(1, len(data_graphe)):
#     if data_graphe.loc[i,'methode_num']==2:
#         data_graphe.loc[i,'nb_chaises']+=0.05
#     elif data_graphe.loc[i,'methode_num']==3:
#         data_graphe.loc[i,'nb_chaises']+=0.10
#     elif data_graphe.loc[i,'methode_num']==4:
#         data_graphe.loc[i,'nb_chaises']+=0.15   



#graphe 2
graphe = px.line(data_graphe, x='iteration',y='nb_chaises', facet_row = 'groupe', facet_col="methode", color='methode')
# graphe.update_yaxes()
graphe.layout.yaxis2.matches = 'y2'
graphe.layout.yaxis6.matches = 'y5'
graphe.layout.yaxis7.matches = 'y5'
graphe.layout.yaxis8.matches = 'y5'
graphe.show()   


#tester avec manuvie, avec grande salle rectangulaire, avec grande salle qui a des division


#creer salle classe grand carré (500 places)
test=[]

for i in range(1,20):
    for j in range(1,10):
        a=[i,"south",i,j,False]
        test.append(a)

for i in range(1,len(salle_classe)):
    test[i][0]=i+1
salle_classe=test