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

#importations qui sont faites dans la classe
import os 

#commentaires
#transformer boolean importation en 0 ? np.array transforme en 0 anyway

#IMPORTATION SALLE
def chairs_list(path):
    #Fonction that create a list of all lines in the file, each line is a list
    data_list = []
    with open(os.path.join(os.getcwd(),"Data",path),"r") as f:
        f.readline() #Skip the 1st line (Header)
        for line in f:
            info = line.rstrip().split("\t")
            data_list.append([int(info[0]), float(info[1]), float(info[2]), bool(0)])
    return data_list


plan_salle = np.array(chairs_list("salle_test54.txt"))

#Voici le graphe des chaises dans la salle de classe
px.scatter(x=plan_salle[:,1],y=plan_salle[:,2], size=([1]*len(plan_salle)),range_x=[0,max(plan_salle[:,1])+1], range_y=[0,max(plan_salle[:,2])+1]) #graphique de la salle

#DÉBUT ALGORITHME

algo_capacite(plan_salle,1000,2)

def algo_capacite(data,iterations,distanciation):
    
    liste_capacite=[] #liste vide pour contenir nombre de chaises retenu par itération 
    list_tableaux=[] #liste vide qui contiendra le plan de salle par itération
    
    for i in range(iterations): #répéter un grande nombre de fois
    
        chaises=data[:,1:4].copy() #initialiser array chaises 
        exclus=np.zeros((len(chaises),3)) #initialiser liste vide exclus

        while (chaises.sum()>0): #pendant qu'il y a encore des chaises encore en jeu 
            en_jeu= (chaises.sum(axis=-1)>0) #boolean chaises  qui sont en jeu
            hors_jeu = (chaises.sum(axis=-1)==0) #boolean chaises qui ne sont plus en jeu
            chaise_hasard = random.choice(chaises[en_jeu]) #choisir chaise au hasard parmi celles en jeu
            chaise_hasard[2]=1 #assigner groupe à 1 
            couple = chaise_hasard[0:2] #x et y de la chaise sélectionnée
            dist_eucl = (chaises[:,0:2] - couple)**2 #différence entre les x,y du couple et ceux de toutes les autres chaises
            dist_eucl = dist_eucl.sum(axis=-1) #somme de la différence x,y
            dist_eucl = np.sqrt(dist_eucl) #racine carrée de la différence
            choisie = ((dist_eucl==0))#boolean chaise choisie
            if hors_jeu.sum()>1: #s'il y a au moins 1 chaise hors jeu 
                dist_eucl[hors_jeu] = np.zeros(hors_jeu.sum()) #dist. eucl. entre couple et chaises hors jeu = 0 
            condition = ((dist_eucl<distanciation) & (dist_eucl>0)) #boolean chaises à <(distanciation)m et >0m
            exclus[condition]=chaises[condition] #ajouter ces chaises trop proche aux eclus
            exclus[choisie] = chaise_hasard #ajouter chaise sélectionnée avec groupe=1 à l'array
            chaises[condition]=np.zeros(((condition.sum()),3)) #retirer couples exclus du array des chaises actives
            chaises[choisie]=np.zeros((1,3)) #retirer chaise choisie du array des chaises actives
    
        liste_capacite.append(exclus[:,2].sum()) #calculer nombre chaises occupées puis ajouter à la liste
        array_final=np.zeros((len(chaises),4)) #créer array rempli de 0 avec 4 colonnes
        array_final[:,1:4]=exclus
        array_final[:,0]=data[:,0]
        array_final_i = array_final 
        list_tableaux.append(array_final_i) #ajouter le tableau des chaises classées à la liste
    
    capacite_optimale=max(liste_capacite) #meilleur nombre de chaises trouvé 
    #meilleure_iteration=liste_capacite.index(capacite_optimale) #meilleure itération parmi le loop
    #meilleur_tableau=list_tableaux[meilleure_iteration] #tableau des groupes de la meilleure itération
    #couples= meilleur_tableau[meilleur_tableau[:,3]==1] #lignes des chaises sélectionnées
    #chaises_choises=list(couples[:,0]) #numéros de chaise sélectionnés
    print(f"La capacité optimale de la salle est de {capacite_optimale:.0f} places") #print capacité optimale



#FIN FONCTION

#graphique de la salle optimale
groups = pd.Categorical(meilleur_tableau[:,3], categories=[0,1], ordered=True)
graph = px.scatter(x=meilleur_tableau[:,1],y=meilleur_tableau[:,2], color=groups, size=([0.5]*len(meilleur_tableau)), range_x=[0,max(plan_salle[:,1])+1], range_y=[0,max(plan_salle[:,2])+1]) 
graph.show()

