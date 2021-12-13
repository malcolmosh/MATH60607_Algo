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
info, salle_classe = test.chairs_list_test(saine)


# algo olivier
optimize1=Voisins_exclus(salle_classe,distance=2, iterations=50, methode=2, division=1, analyse_perfo=True)
tableau, temps = optimize1.optimize()
optimize1.resultat()
#optimize1.graphe_sortie()
optimize1.temps()
optimize1.tableau_perfo
#optimize1.tous_groupes

optimize1.tableau_perfo.to_excel("file.xlsx")

#optimize1.graphe_sortie()
# tous_groupes = optimize1.tous_groupes
# #
# # optimize1.tous_groupes
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
            optimize1=Voisins_exclus(salle_classe,distance=distance,iterations=iterations,methode=i, division=division, analyse_perfo=True)
            optimize1.optimize()
            tableau_perfo=optimize1.tableau_perfo
            tableau_perfo['epoch']=epoch
            #tous_groupes=[row for row in tous_groupes]
            meta_liste.append(tableau_perfo)
        meta_liste=pd.concat(meta_liste)
        meta_liste.reset_index(inplace=True, drop=True)
        meta_liste_2.append(meta_liste)

    #créer dataframe
    data_graphe=pd.concat(meta_liste_2)
    data_graphe.reset_index(inplace=True, drop=True)
    #data_graphe = pd.DataFrame(np.concatenate(np.concatenate(meta_liste_2)),columns=['epoch', 'groupe', 'iteration','nb_chaises','methode_num'])
    
    #ajouter nom methode
    data_graphe['Methode_txt'] = data_graphe['Methode'].map({1:"Voisin aléatoire",2:"Plus proche voisin",3:"Plus loin voisin",4:"Plus proche voisin pondéré", 5:"Plus loin voisin pondéré"}) 
    #data_graphe.columns
    #pour box plot 
    data_boite_moustache = data_graphe.groupby(["Methode","epoch"], as_index=False).max()
    data_boite_moustache= data_boite_moustache.drop(columns=["Num_groupe","Num_iter","Methode"])
    #data_graphe[data_graphe['nb_chaises']==13]

    #écraser les groupes au travers des epoch, methode et iterations
    data_graphe = data_graphe.groupby(["epoch","Methode", "Methode_txt", "Num_iter"], as_index=False).sum()
    data_graphe=data_graphe.drop(columns="Num_groupe")
    
    #ajuster avec le maximum 
    #remplacer le nombre de chaises dans chaque epoch, méthode et dans chaque groupe par le maximum, une fois qu'il est atteint
    #sert dans le cas des graphes de performance avec division=1. Quand il y a qu'une chaise dans un groupe, elle atteint son max à l'itération 0 et arrête à 50
    #d'autres groupes vont arrêter plus loin, il faut donc ajuster le graphe
    data_np = np.array(data_graphe)
    data_graphe.columns
    for i in range (1,len(data_np)):
        if data_np[i,0]==data_np[i-1,0] and data_np[i,1]==data_np[i-1,1]: #si epoch, methode sont pareis
            if data_np[i,4]<=data_np[i-1,4]: #si meilleur résultat itération précédente, remplacer
                data_np[i,4]=data_np[i-1,4]

    #reconvertir en pandas
    data_graphe = pd.DataFrame(data_np, columns=data_graphe.columns)
    
    #moyenne au travers des méta-loops
    data_graphe= data_graphe.groupby(['Methode','Methode_txt','Num_iter'],as_index=False).mean()
    data_graphe = data_graphe.drop(columns="epoch")
    data_graphe.reset_index(inplace=True)
    
    #max chaises
    max_chaises_atteint = data_graphe['Best_somme_atteinte'].max() 
    
    # # #offset values by methode
    for i in range(1, len(data_graphe)):
        if data_graphe.loc[i,'Methode']==4:
            data_graphe.loc[i,'Best_somme_atteinte']+=0.03
        elif data_graphe.loc[i,'Methode']==5:
             data_graphe.loc[i,'Best_somme_atteinte']-=0.03
    
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

    return(titre, details, data_graphe, data_boite_moustache, max_chaises_atteint)
            
def generer_graphe(titre, details, data, max_chaises_atteint):
    #config affichage
    config = {'toImageButtonOptions': {'format': 'png', # one of png, svg, jpeg, webp
        'filename': 'plot',
        'scale': 5 }} # Multiply title/legend/axis/canvas sizes by this factor 
    #produire graphe
    graphe = px.line(data, x='Num_iter',y='Best_somme_atteinte', color="Methode_txt", 
                     labels=dict(Num_iter="Itération", Best_somme_atteinte="Capacité calculée", Methode_txt="Méthode"), 
                     title=titre+"<br><sup>"+details+"</sup>")
                     #color_discrete_sequence=px.colors.qualitative.G10)
    graphe.update_traces(mode="lines", line_shape="vh", line=dict(width=4))
    #graphe.add_hline(y=max_chaises_atteint, line_dash="dot", annotation_text="Max. moyen atteint :"+str(round(max_chaises_atteint,2))+" chaises", annotation_position="top left", line_color="red")
   # graphe.update_xaxes(range=[0,derniere_iter_max+10])
    nom_fichier=(titre+details[11:24]).replace(" ","_")
    graphe.show(config=config)   
    #import kaleido
    #graphe.write_image("Graphes/"+nom_fichier+".png",engine="kaleido", scale=5)

def generer_barplot(data):    
    #config affichage
    config = {'toImageButtonOptions': {'format': 'png', # one of png, svg, jpeg, webp
        'filename': 'plot',
        'scale': 5 }} # Multiply title/legend/axis/canvas sizes by this factor 
    #produire graphe  pour comparer le nombre de chaise atteint au travers des méta-itérations
    data2=data.groupby(["Methode_txt","Best_somme_atteinte"], as_index=False).count()
    data2['Best_somme_atteinte']=pd.Categorical(data2['Best_somme_atteinte'].astype(int))
    fig = px.bar(data2,x="Methode_txt", y="epoch", color="Best_somme_atteinte",
                 title=titre+"<br><sup>"+details+"</sup>",
                 labels=dict(epoch="Nombre de méta-itérations", Best_somme_atteinte="Capacité calculée", Methode="Méthode utilisée"))
    fig.update_layout(barmode='group')
    #nom_fichier=(("(BAR)")+titre+details[11:24]).replace(" ","_")
    #fig.write_image("Graphes/"+nom_fichier+".png")
    #import kaleido
    #nom_fichier=(titre+details[11:24]).replace(" ","_")
    #fig.write_image("Graphes/"+nom_fichier+"_bar.png",engine="kaleido", scale=5)
    fig.show(config=config)


#générer les données
titre, details, data_graphe, data_boxplot, max_chaises_atteint = generer_donnees(salle=saine, metaloops=1, distance=2, iterations=50, division=1)

#produire le graphe de performance
generer_graphe(titre=titre, details=details, data=data_graphe, max_chaises_atteint=max_chaises_atteint)

#produire le graphe de comparaisons des résultats au travers des méta-itérations
generer_barplot(data=data_boxplot)