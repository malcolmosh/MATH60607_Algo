#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 18:22:39 2021

@author: osher
"""

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
mega="Salle Mega 1105.txt"
banque= "Salle Banque Scotia.txt"
cogeco = "Salle Cogeco.txt"
manuvie = "Salle Manuvie.txt"
saine = "Salle Saine Marketing.txt"
info, salle_classe = test.chairs_list_test(banque)


# algo olivier
optimize1=Voisins_exclus(salle_classe,distance=2, iterations=500, methode=4, division=0)
tableau, temps = optimize1.optimize()
optimize1.resultat()
optimize1.graphe_sortie()
optimize1.temps()


#optimize1.graphe_sortie()
# tous_groupes = optimize1.tous_groupes
# #
# # optimize1.tableau_perfo
# optimize1.interruption()
# # optimize1.graphe_entree()


#générer données 
def generer_donnees(salle, metaloops, distance, iterations, division):

    test=Salles(app=False)
    info, salle_classe = test.chairs_list_test(salle)

    meta_liste_2=[]
    for epoch in range(1,metaloops+1):
        meta_liste=[]
        #boucle méthodes
        for i in range(1,6):
            optimize1=Voisins_exclus(salle_classe,distance=distance,iterations=iterations,methode=i, division=division)
            optimize1.optimize()
            tous_groupes = [[epoch]+row for row in optimize1.tous_groupes]
            #tous_groupes=[row for row in tous_groupes]
            meta_liste.append(tous_groupes)
        meta_liste_2.append(meta_liste)
    
    #créer dataframe
    data_graphe = pd.DataFrame(np.concatenate(np.concatenate(meta_liste_2)),columns=['epoch', 'groupe', 'iteration','nb_chaises','methode_num'])
    
    #data_graphe[data_graphe["nb_chaises"]==15]['methode_num'].unique()
    
    #ajouter nom methode
    data_graphe['methode'] = data_graphe['methode_num'].map({1:"Voisin aléatoire",2:"Plus proche voisin",3:"Plus loin voisin",4:"Plus proche voisin pondéré", 5:"Plus loin voisin pondéré"}) 
 
    #pour box plot 
    data_boite_moustache = data_graphe.groupby(["methode","epoch"], as_index=False).max()
    data_boite_moustache= data_boite_moustache.drop(columns=["groupe","iteration","methode_num"])
    #data_graphe[data_graphe['nb_chaises']==13]

    #écraser les groupes au travers des epoch, methode et iterations
    data_graphe = data_graphe.groupby(["epoch","methode_num", "methode", "iteration"], as_index=False).sum()
    data_graphe=data_graphe.drop(columns="groupe")
    
    #data_graphe[data_graphe["nb_chaises"]==15]['methode_num'].unique()
    
    #remplacer le nombre de chaises dans chaque epoch, méthode et dans chaque groupe par le maximum, une fois qu'il est atteint
    data_np = np.array(data_graphe)
    data_graphe.columns
    for i in range (1,len(data_np)):
        if data_np[i,0]==data_np[i-1,0] and data_np[i,1]==data_np[i-1,1]: #and data_np[i,4]==data_np[i-1,4]:
            if data_np[i,4]<=data_np[i-1,4]:
                data_np[i,4]=data_np[i-1,4]

    #reconvertir en pandas
    data_graphe = pd.DataFrame(data_np, columns=data_graphe.columns)
    
    #moyenne au travers des méta-loops
    data_graphe= data_graphe.groupby(['methode','methode_num','iteration'],as_index=False).mean()
    data_graphe = data_graphe.drop(columns="epoch")
    data_graphe.reset_index(inplace=True)
    

    #max chaises
    max_chaises_atteint = data_graphe['nb_chaises'].max() 
    #trouver l'itération maximale à laquelle une des méthodes finit par converger à 100% (pour ajuster axes)
    ### À REVOIR
    derniere_iter_max = data_graphe[data_graphe['nb_chaises']==max_chaises_atteint].groupby("methode_num").first()['iteration'].max()
    
    # # #offset values by methode
    for i in range(1, len(data_graphe)):
        if data_graphe.loc[i,'methode_num']==2:
            data_graphe.loc[i,'nb_chaises']+=0.01
        elif data_graphe.loc[i,'methode_num']==3:
            data_graphe.loc[i,'nb_chaises']-=0.01
        elif data_graphe.loc[i,'methode_num']==4:
            data_graphe.loc[i,'nb_chaises']+=0.02
    
    #division
    if division==1:
        indicateur_div="avec division"
    else:
        indicateur_div="sans division"
        
    #titre salle
    if salle==mega:
        titre="Grande salle (1105 sièges)"
    elif salle==banque:
        titre="Salle Banque Scotia (70 sièges)"
    elif salle==cogeco:
        titre="Salle Cogeco (31 sièges)"
    elif salle==manuvie:
        titre="Salle Manuvie (55 sièges)"
    elif salle==saine:
        titre="Salle Saine Marketing (56 sièges)"
        
    #details
    details="Distance: "+str(distance)+"m., "+indicateur_div+", "+str(metaloops)+" méta-itérations, "+str(iterations)+" itérations"

    return(titre, details, data_graphe, derniere_iter_max, data_boite_moustache, max_chaises_atteint)
            
def generer_graphe(titre, details, data, derniere_iter_max, max_chaises_atteint):
    #config affichage
    config = {'toImageButtonOptions': {'format': 'png', # one of png, svg, jpeg, webp
        'filename': 'plot',
        'scale': 5 }} # Multiply title/legend/axis/canvas sizes by this factor 
    #produire graphe
    graphe = px.line(data, x='iteration',y='nb_chaises', color="methode", 
                     labels=dict(iteration="Itération", nb_chaises="Capacité calculée", methode="Méthode"), 
                     title=titre+"<br><sup>"+details+"</sup>")
                     #color_discrete_sequence=px.colors.qualitative.G10)
    graphe.update_traces(mode="lines", line_shape="vh", line=dict(width=4))
    #graphe.add_hline(y=max_chaises_atteint, line_dash="dot", annotation_text="Max. moyen atteint :"+str(round(max_chaises_atteint,2))+" chaises", annotation_position="top left", line_color="red")
   # graphe.update_xaxes(range=[0,derniere_iter_max+10])
    nom_fichier=(titre+details[11:24]).replace(" ","_")
    graphe.show(config=config)   
    import kaleido
    graphe.write_image("Graphes/"+nom_fichier+".png",engine="kaleido", scale=5)

def generer_barplot(data):    
    #config affichage
    config = {'toImageButtonOptions': {'format': 'png', # one of png, svg, jpeg, webp
        'filename': 'plot',
        'scale': 5 }} # Multiply title/legend/axis/canvas sizes by this factor 
    #produire graphe  pour comparer le nombre de chaise atteint au travers des méta-itérations
    data2=data.groupby(["methode","nb_chaises"], as_index=False).count()
    data2['nb_chaises']=pd.Categorical(data2['nb_chaises'].astype(int))
    fig = px.bar(data2,x="methode", y="epoch", color="nb_chaises",
                 title=titre+"<br><sup>"+details+"</sup>",
                 labels=dict(epoch="Nombre de méta-itérations", nb_chaises="Capacité calculée", methode="Méthode utilisée"))
    fig.update_layout(barmode='group')
    #nom_fichier=(("(BAR)")+titre+details[11:24]).replace(" ","_")
    #fig.write_image("Graphes/"+nom_fichier+".png")
    import kaleido
    nom_fichier=(titre+details[11:24]).replace(" ","_")
    fig.write_image("Graphes/"+nom_fichier+"_bar.png",engine="kaleido", scale=5)
    fig.show(config=config)

#faire graphe 
titre, details, data_graphe, derniere_iter_max, data_boxplot, max_chaises_atteint = generer_donnees(salle=banque, metaloops=1, distance=2, iterations=10000, division=0)

generer_graphe(titre=titre, details=details, data=data_graphe, derniere_iter_max=derniere_iter_max, max_chaises_atteint=max_chaises_atteint)

generer_barplot(data=data_boxplot)

#comparatif temps
# #PAS parallèle
# from All_class.class_voisins_exclus import Voisins_exclus
# info, salle_classe = test.chairs_list_test(mega)
# optimize1=Voisins_exclus(salle_classe,distance=2, iterations=5000, methode=1, division=1)
# tableau, temps = optimize1.optimize()
# temps_non_para=temps

# #parallélisé
# from All_class.class_voisins_exclus_para import Voisins_exclus
# info, salle_classe = test.chairs_list_test(mega)
# optimize1=Voisins_exclus(salle_classe,distance=2, iterations=5000, methode=1, division=1)
# tableau, temps = optimize1.optimize()
# temps_para=temps

# data_parallele=pd.DataFrame((round(temps_non_para,1),round(temps_para,1)), columns=["Temps en secondes"])
# data_parallele['Stratégie']=["Non parallélisé", "Parallélisé"]

# #
# fig = px.bar(data_parallele,x="Stratégie", y="Temps en secondes",title="Performance de la parallélisation - salle de 1105 sièges divisée en groupes,5000 itérations")
# fig.show()

#https://stackoverflow.com/questions/21027477/joblib-parallel-multiple-cpus-slower-than-single
