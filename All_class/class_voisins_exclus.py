#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 17:19:59 2021

@author: osher
"""
## importation packages
#pour optiimisation
import random #sélection aléatoire
import numpy as np
import time
 
#pour graphe
import plotly.io as pio
import plotly.express as px
pio.renderers.default='browser' #pour générer graphiques plotly dans browser
import pandas as pd

#créer classe
class Voisins_exclus:
    
    def __init__(self, data,distance,iterations=500, maximum_time=5, methode=1):
        self.data = data
        self.distance = distance
        self.iterations = iterations
        self.maximum_time = maximum_time
        self.methode=methode
        self.tableau_optimal = () #vecteur qui contiendra la meilleure sortie de l'algorithme
        
    #vérifier si les listes du début sont vides ou pas
    #voir https://stackoverflow.com/questions/32836291/check-if-object-attributes-are-non-empty-python
    def __nonzero__(self): 
        return bool(self.tableau_optimal)
    
    #rouler l'algorithme
    def optimize(self):    
        data=(self.data) #fichier donnees en entree
       
        #liste vide pour entreposer les orientations
        orientations = [] 
        
        # retirer la colonne des points cardinaux du fichier de données
        for row in data: 
            orientations.append(row[1]) #ajouter le point cardinal à la liste
            del row[1] 
        
        #conversion en array
        data=np.array(data)
        liste_capacite=[] #liste vide pour contenir nombre de chaises retenu par itération 
        list_tableaux=[] #liste vide qui contiendra le array final par itération
         
        #vérifier l'heure
        start=time.time()
        #début de la boucle - répéter autant de fois qu'il y a d'itérations
        for i in range(self.iterations): 
            chaises=data[:,1:4].copy() #initialiser array chaises 
            exclus=np.zeros((len(chaises),3)) #initialiser liste vide exclus
    
            while_index = 0 #index des boucles du while

            while (chaises.sum()>0): #pendant qu'il y a encore des chaises encore en jeu 
                en_jeu= (chaises.sum(axis=-1)>0) #boolean chaises qui sont en jeu
                hors_jeu = (chaises.sum(axis=-1)==0) #boolean chaises qui ne sont plus en jeu
                
                if self.methode==2 and while_index>0:  #si algorithme plus proche voisin est choisi et si on est à la 2e boucle while 
                    #trouver plus proche voisin
                    voisins = dist_eucl[(dist_eucl>self.distance)] # retenir toutes les chaises à plus de 2m
                    dist_proche_voisin = min(voisins) #trouver voisin le plus proche (si il y en a deux, au hasard)
                    index = dist_eucl.tolist().index(dist_proche_voisin) #index de cette chaise dans la liste des distances euclidiennes
                    chaise_hasard = chaises[index]  #désigner la prochaine chaise : sélectionner la proche chaise dans le array des chaises en jeu
         
                else: #méthode==1
                    chaise_hasard = random.choice(chaises[en_jeu]) #choisir chaise au hasard parmi celles en jeu
                
                chaise_hasard[2]=1 #assigner groupe à 1 
                couple = chaise_hasard[0:2] #x et y de la chaise sélectionnée
                dist_eucl = (chaises[:,0:2] - couple)**2 #différence entre les x,y du couple et ceux de toutes les autres chaises
                dist_eucl = dist_eucl.sum(axis=-1) #somme de la différence x,y
                dist_eucl = np.sqrt(dist_eucl) #racine carrée de la différence
                choisie = ((dist_eucl==0))#boolean chaise choisie
                if hors_jeu.sum()>1: #s'il y a au moins 1 chaise hors jeu 
                    dist_eucl[hors_jeu] = np.zeros(hors_jeu.sum()) #dist. eucl. entre couple et chaises hors jeu = 0 
                condition = ((dist_eucl<self.distance) & (dist_eucl>0)) #boolean chaises à <(distanciation)m et >0m
                exclus[condition]=chaises[condition] #ajouter ces chaises trop proche aux exclus
                exclus[choisie] = chaise_hasard #ajouter chaise sélectionnée avec groupe=1 à l'array
                chaises[condition]=np.zeros(((condition.sum()),3)) #retirer couples exclus du array des chaises actives
                chaises[choisie]=np.zeros((1,3)) #retirer chaise choisie du array des chaises actives
            
                while_index+=1

            
            #enregistrer les sorties
            liste_capacite.append(exclus[:,2].sum()) #calculer nombre chaises occupées puis ajouter à la liste
            array_final=np.zeros((len(chaises),4)) #créer array rempli de 0 avec 4 colonnes
            array_final[:,1:4]=exclus #ajouter le choix final des chaises à ce nouvel array, array_final
            array_final[:,0]=data[:,0] # ajouter le numero de chaise en première colonne de l'array final
            array_final_i = array_final # ajouter le numero de l'itération à l'array actuel 
            list_tableaux.append(array_final_i) #ajouter le tableau final des chaises classées à la liste
            
            time_now = time.time() #moment de fin de l'itération 
            potential_end = (time_now - start)/60 #temps écoulé en minutes depuis le début de l'algorithme
           
           #si le temps dépasse le temps maximum fourni en paramètre, arrêter à la fin de l'itération
            if potential_end >= self.maximum_time:
                interrompu=1
                break
            else:
                interrompu=0
            
        # retenir meilleur résultat        
        capacite_optimale=max(liste_capacite) #meilleur nombre de chaises trouvé 
        meilleure_iteration=liste_capacite.index(capacite_optimale) #meilleure itération parmi le loop
        meilleur_tableau=list_tableaux[meilleure_iteration] #tableau des groupes de la meilleure itération
        meilleur_tableau = meilleur_tableau.tolist() #convertir en liste
        
        #boucle pour ajouter l'orientation des chaises au tableau final
        for index, row in enumerate(meilleur_tableau):
            row.insert(1,orientations[index])
            
        #calculer temps écoulé pour tout l'algorithme
        end=time.time()
        total_time = (end - start)

        #entreposer les variables pour les réutiliser dans les méthodes suivantes
        self.tableau_optimal = meilleur_tableau
        self.total_time = total_time
        self.capacite_optimale = capacite_optimale
        self.interrompu = interrompu
        self.potential_end = potential_end
        
        #sortie finale : on retourne le meilleur tableau et le temps écoulé
        liste_finale = []
        liste_finale.append(self.tableau_optimal)
        liste_finale.append(self.total_time)
        return liste_finale
    
    #imprimer le résultat de la meilleure itération
    def resultat(self): 
        if len(self.tableau_optimal)==0: #si l'algorithme n'a pas roulé encore
            print("Vous devez d'abord utiiser rouler() pour lancer l'algorithme")
        else: #si on a roulé l'algorithme déjà, produire la meilleure sortie
            somme = self.capacite_optimale
            print(f"La capacité optimale de la salle est de {somme:.0f} places") #print capacité optimale
   
    #indiquer si l'algorithme a été interrompu ou non
    def interruption(self): 
        if (self.interrompu)==0: #si l'algorithme n'a pas roulé encore
            print("L'algorithme n'a pas été interrompu")
        else: #si on a roulé l'algorithme déjà, produire la meilleure sortie
            print(f"L'algorithme a été interrompu à {round((self.potential_end/60),5)} minutes") 

    #imprimer temps écoulé 
    def temps(self): 
        if len(self.tableau_optimal)==0: #si l'algorithme n'a pas roulé encore
            print("Vous devez d'abord utiiser rouler() pour lancer l'algorithme")
        else: #si on a roulé l'algorithme déjà, produire le temps écoulé
            print(f"Temps écoulé : {round(self.total_time,2)} secondes") 

    # #array de la meilleure itération
    # def tableau(self): 
    #     if len(self.tableau_optimal)==0: #si l'algorithme n'a pas roulé encore
    #         print("Vous devez d'abord utiiser rouler() pour lancer l'algorithme")
    #     else: #si on a roulé l'algorithme déjà, produire la meilleure sortie
    #         return(self.tableau_optimal)
        
    #graphe initial de la salle sans assignations de chaise
    def graphe_entree(self): 
        if len(self.tableau_optimal)==0: #si l'algorithme n'a pas roulé encore
            print("Vous devez d'abord utiiser rouler() pour lancer l'algorithme")
        else: #si on a roulé l'algorithme déjà, sortir le graphique initial
            tableau = self.tableau_optimal
            x_cord = [row[2] for row in tableau]
            y_cord = [row[3] for row in tableau]
            graphe = px.scatter(x=x_cord,y=y_cord,range_x=[0,max(x_cord)+1], size = [1]*len(tableau), range_y=[0,max(y_cord)+1]) 
            graphe.show()   
            
    #graphe de la salle en sortie avec les assignations de chaise
    def graphe_sortie(self): 
        if len(self.tableau_optimal)==0: #si l'algorithme n'a pas roulé encore
            print("Vous devez d'abord utiiser rouler() pour lancer l'algorithme")
        else: #si on a roulé l'algorithme déjà, sortir le graphique final
            tableau = self.tableau_optimal
            x_cord = [row[2] for row in tableau]
            y_cord = [row[3] for row in tableau]
            groups = pd.Categorical([row[4] for row in tableau], categories=[0,1], ordered=True)
            graphe = px.scatter(x=x_cord,y=y_cord,color=groups, size = [1]*len(tableau), range_x=[0,max(x_cord)+1], range_y=[0,max(y_cord)+1]) 
            graphe.show()   

       