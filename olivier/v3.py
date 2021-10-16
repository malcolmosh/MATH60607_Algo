#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 17:23:33 2021

@author: osher
"""

from datetime import datetime #calculer temps éxécution
import pandas as pd
import numpy as np
import plotly.io as pio
import plotly.express as px
pio.renderers.default='browser' #pour générer graphiques plotly dans browser
import itertools

# start=datetime.now() #calculer temps éxécution


#On commence par initialiser une salle de cours carrée, en construisant deux vecteurs.
longueur = list(range(5,15)) #un vecteur qui représente en mètres la position des chaises sur la longueur
hauteur = list(range(5,15)) #un vecteur qui représente en mètres la position des chaises sur la hauteur
combinaisons = list(itertools.product(longueur,hauteur)) #créer toutes les combinaisons de variables possibles. 


#Voici le graphe des chaises dans la salle de classe
#px.scatter(x=np.array(combinaisons)[:,0],y=np.array(combinaisons)[:,1], size=([1]*len(combinaisons)),range_x=[0,max(longueur)+1], range_y=[0,max(hauteur)+1]) #graphique de la salle


#ALGORITHME


list_values=[] #liste vide pour contenir nombre de chaises retenu par itération 
list_tableaux=[] #liste vide qui contiendra un tableau des chaises occupées par itération

for i in range(100): #itérer à travers l'algorithme un grande nombre de fois

    tableau = pd.DataFrame(combinaisons) #transformer en df
    tableau[2]=([0]*len(combinaisons)) #ajouter colonne groupe (0=libre, 1=occupé)
    tableau.columns=("Largeur","Longueur","Groupe") #nommer colonnes
    tableau["Groupe"]=pd.Categorical(tableau["Groupe"], categories=[0,1], ordered=True) #transfo en variable catégorielle
    exclus=tableau.loc[tableau["Groupe"]==1] #initialiser liste vide de chaises exclues (chaque chaise est un couple x,y)
    tableau_actif=tableau #initialiser liste de couples actifs

    while len(tableau_actif>=1): #pendant qu'il y a encore des chaises en jeu 
        num_ligne = tableau_actif.sample().index[0] #choisir chaise au hasard
        tableau.iloc[[num_ligne],2]=1 #assigner groupe à 1
        couple = tableau.iloc[num_ligne,0:2].values #obtenir couple de valeurs de cette chaise occupée
        dist= np.sqrt(((tableau_actif.iloc[:,0].values-couple[0])**2)+((tableau_actif.iloc[:,1].values-couple[1])**2)) #distance euclidienne de la chaise avec toutes les autres actives
        exclus2 = tableau_actif.loc[dist<2,:] #exclure couples à moins de 2 mètres parmi les couples actifs
        exclus = pd.concat([exclus,exclus2]) #concaténer les nouveaux couples exclus aux anciens
        tableau_actif = tableau.loc[~tableau.index.isin(exclus.index)] #mettre à jour tableau couples actifs
    
    list_values.append((tableau["Groupe"]==1).sum()) #calculer nombre chaises occupées puis ajouter à la liste
    tableau_i = tableau 
    list_tableaux.append(tableau_i) #ajouter le tableau des chaises classées à la liste
    
#FIN ALGORITHME

meilleur_nombre=max(list_values) #meilleur nombre de chaises trouvé 
meilleure_iteration=list_values.index(meilleur_nombre) #meilleure itération parmi le loop
meilleur_tableau=list_tableaux[meilleure_iteration] #tableau des groupes de la meilleure itération
couples= meilleur_tableau.loc[(meilleur_tableau["Groupe"]==1),["Longueur","Largeur"]].values #sortir couples de chaises occupées
# print(list_values)
# print(couples)
print(meilleur_nombre)

# print( datetime.now()-start ) #calculer temps éxécution

#graphique de la salle optimale
#px.scatter(meilleur_tableau,x="Largeur",y="Longueur", color="Groupe", size=([1]*len(meilleur_tableau)), range_x=[0,max(longueur)+1], range_y=[0,max(hauteur)+1]) 

#transformer en fonction
#raffiner graphique, paralléliser ?

