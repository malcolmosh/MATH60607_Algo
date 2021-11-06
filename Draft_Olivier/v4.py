#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 12:20:38 2021

@author: osher
"""
#from datetime import datetime #calculer temps éxécution
import pandas as pd
import numpy as np
import plotly.io as pio
import plotly.express as px
pio.renderers.default='browser' #pour générer graphiques plotly dans browser
import itertools
import random #sélection aléatoire

#start=datetime.now() #calculer durée 

#On commence par initialiser une salle de cours carrée, en construisant deux vecteurs.

n=10 #longueur du côté du carré
#m_longueur = list(range(5,5+n)) #un vecteur qui représente en mètres la position des chaises sur la longueur
#m_hauteur = list(range(5,5+n)) #un vecteur qui représente en mètres la position des chaises sur la hauteur

m_longueur = list(range(2,13)) #un vecteur qui représente en mètres la position des chaises sur la longueur
m_hauteur = list(range(2,20)) #un vecteur qui représente en mètres la position des chaises sur la hauteur


combinaisons = list(itertools.product(m_longueur,m_hauteur)) #créer toutes les combinaisons de variables possibles. 

groupe = np.zeros((len(combinaisons),3)) #initialiser array de zéros avec même nbr lignes que combinaisons, mais 1 colonne de plus
groupe[:,:-1] = combinaisons #remplir 2 premières colonnes de groupe par les couples de combinaisons
groupes_chaises = groupe #df principal

#Voici le graphe des chaises dans la salle de classe
px.scatter(x=groupes_chaises[:,0],y=groupes_chaises[:,1], size=([1]*len(combinaisons)),range_x=[0,max(m_longueur)+1], range_y=[0,max(m_hauteur)+1]) #graphique de la salle

#ALGORITHME

list_values=[] #liste vide pour contenir nombre de chaises retenu par itération 
list_tableaux=[] #liste vide qui contiendra un tableau des chaises occupées par itération

for i in range(500): #itérer à travers l'algorithme un grande nombre de fois

    exclus=np.zeros((len(combinaisons),3)) #initialiser des exclus (pleine de 0)
    chaises_actives=groupes_chaises.copy() #initialiser array chaises actives

    while (chaises_actives.sum()>0): #pendant qu'il y a encore des chaises en jeu 
        pas_vides= (chaises_actives.sum(axis=-1)>0) #boolean chaises actives qui ne sont pas vides (égales à zéro, retirées de l'itération précédente)
        vides = (chaises_actives.sum(axis=-1)==0) #boolean chaises actives qui ont été retirées
        chaise_hasard = random.choice(chaises_actives[pas_vides]) #choisir chaise au hasard parmi celles du ne sont pas vides
        chaise_hasard[2]=1 #assigner groupe à 1 
        couple = chaise_hasard[0:2] #x et y de la chaise sélectionnée
        dist_eucl = (chaises_actives[:,0:2] - couple)**2 #différence entre chaque x et y de l'array et le couple
        dist_eucl = dist_eucl.sum(axis=-1) #somme de la différence
        dist_eucl = np.sqrt(dist_eucl) #racine carrée de la différence
        choisie = ((dist_eucl==0))#boolean chaise choisie
        if vides.sum()>1: 
            dist_eucl[vides] = np.zeros(vides.sum()) #np.zeros(((vides.sum()),1)) #assigner à 0 les distances eucl. avec les chaises retirées déjà
        condition = ((dist_eucl<2) & (dist_eucl>0)) #boolean chaises <2m et >0m
        exclus[condition]=chaises_actives[condition] #ajouter couples <2m et >0 au array des couples exclus
        exclus[choisie] = chaise_hasard #ajouter chaise sélectionnée avec groupe=1 à l'array
        chaises_actives[condition]=np.zeros(((condition.sum()),3)) #retirer couples exclus du array des chaises actives
        chaises_actives[choisie]=np.zeros((1,3)) #retirer chaise choisie du array des chaises actives

    list_values.append(exclus[:,2].sum()) #calculer nombre chaises occupées puis ajouter à la liste
    tableau_i = exclus 
    list_tableaux.append(tableau_i) #ajouter le tableau des chaises classées à la liste
    
#FIN ALGORITHME #REPRENDRE ICI

meilleur_nombre=max(list_values) #meilleur nombre de chaises trouvé 
meilleure_iteration=list_values.index(meilleur_nombre) #meilleure itération parmi le loop
meilleur_tableau=list_tableaux[meilleure_iteration] #tableau des groupes de la meilleure itération
couples= meilleur_tableau[meilleur_tableau[:,2]==1]
print(meilleur_nombre)

#graphique de la salle optimale
groups = pd.Categorical(meilleur_tableau[:,2], categories=[0,1], ordered=True)
graph = px.scatter(x=meilleur_tableau[:,0],y=meilleur_tableau[:,1], color=groups, size=([0.5]*len(meilleur_tableau)), range_x=[0,max(m_longueur)+1], range_y=[0,max(m_hauteur)+1]) 
graph.show()

#print( datetime.now()-start ) #calculer durée



