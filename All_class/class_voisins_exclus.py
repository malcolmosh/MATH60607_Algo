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
    
    def __init__(self, data,distance,iterations=500, maximum_time=5, methode=1, division=0, analyse_perfo=False):
        self.data = data
        self.distance = distance
        self.iterations = iterations
        self.maximum_time = maximum_time
        self.methode=methode
        self.division = division
        self.tableau_optimal=()
        self.analyse_perfo=analyse_perfo
        
    #vérifier si les listes du début sont vides ou pas
    def __nonzero__(self): 
        return bool(self.tableau_optimal)
    
    #rouler l'algorithme
    def optimize(self):    
        donnees=(self.data) #fichier donnees en entree
       
        #vérifier l'heure
        start=time.time()

        # entreposer les orientations (south,west,east,north)
        orientations = [row[1] for row in donnees]
        # retirer la colonne des orientations du fichier de données   
        donnees = [[row[0], row[2], row[3], row[4]] for row in donnees]
        
        #si on ne divise pas la classe, tous les chaises sont dans le même groupe (1)
        if self.division==0: 
            donnees = [row+[1] for row in donnees] 
            donnees = np.array(donnees)
            
        #sinon, on divise la classe en section
        else:
            #ajouter colonne groupe=0 (num, pos_x, pos_y, groupe)
            donnees = [row+[0] for row in donnees]
            donnees = np.array(donnees)
        
            f=0 #group number holder
            #print(data_dataframe)
            for n in range(0,len(donnees)):
                #itérer à travers toutes les chaises 
                if donnees[n,4]==0: #si groupe est 0 
                    f+=1 
                    donnees[n,4]=f #assigner premier groupe
                    L=[n]
                    #pour chaque chaise initiale plus toute chaise assignée à un groupe dans cette itération
                    for i in L: 
                        #pour chaque paire de chaise
                        for j in range(0,len(donnees)):
                            #calculer distance euclidienne
                            distance_pair=((((donnees[i,1]-donnees[j,1])**2)+((donnees[i,2]-donnees[j,2])**2))**0.5)
                            if i!=j and donnees[j,4]==0 and (distance_pair < self.distance):
                                donnees[j,4]=f
                                L.append(j) #ajouter ces chaises à la liste pour qu'on donne le même groupe aux chaises à moins de deux mètres
                                     
        #nombre de groupes
        nombre_groupes = set(donnees[:,4].tolist()) 
        
        #indicateur d'amélioration successive pour analyser performance
        tableau_perfo=[]
            
        #boucle pour chaque groupe
        def calcul_groupe(i):
        
            #sélectionner les chaises de ce groupe
            subset = donnees[np.where(donnees[:,4] ==i)]
            
            #entroposer le meilleur tableau du groupe dans un array
            meilleur_tableau=subset[:,0:4].copy()
            #entreposer la meilleure somme de chaises occupées
            meilleure_somme=meilleur_tableau[:,3].sum()

            for j in range(self.iterations): 
                
                #initialiser tableau initial des chaises du sous-groupe, avec 4 colonnes (num, x, y, occupation)
                tableau_initial=subset[:,0:4].copy() 
                #initialiser liste vide de chaises. nous allons vider la liste initiale peu à peu pour déplacer les chaises vers cette liste finale. 
                tableau_final=np.zeros((len(tableau_initial),4))
                #créer un indicateur des boucles du while
                while_index = 0 
                

                while (tableau_initial[:,1:4].sum()>0): #pendant qu'il y a encore des chaises encore en jeu 
                    en_jeu= (tableau_initial[:,1:4].sum(axis=-1)>0) #boolean chaises qui sont en jeu
                    hors_jeu = (tableau_initial[:,1:4].sum(axis=-1)==0) #boolean chaises qui ne sont plus en jeu
                    
                    #sélection prochaine chaise (1=au hasard, 2=plus proche voisin, 3 = plus loin voisin, 4 = plus proche voisin pondéré, 5 = plus loin voisin pondéré))
                        
                    #si il n'y a q'une ou deux chaises dans ce groupe
                    if len(subset)==1 or len(subset)==2: 
                        subset[0,3]=1 #assigner première chaise comme occupée 
                        tableau_final=subset[:,0:4]
                        tableau_initial[0:4]=[0,0,0,0]
                        
                    #sinon utilisons la méthode spécifiée
                    else:

                        #plus proche voisin et si plus d'une chaise en jeu
                        if self.methode==2 and sum(en_jeu)>1:
                           
                            #si première boucle
                            if while_index==0: 
                                prochaine_chaise = tableau_initial[0] #choisir chaise #1 (baseline)
                            
                            #si 2e et + boucle
                            else:
                                voisins = dist_eucl[en_jeu] # retenir toutes les chaises à plus de la distance spécifiée 
     
                                if (min(voisins)==max(voisins)): #si voisins min et max sont à la même distance
                                    prochaine_chaise = random.choice(tableau_initial[en_jeu]) #choisir au hasard 
        
                                else:                  
                                    dist_proche_voisin = min(voisins) #trouver voisin le plus proche (si il y en a deux, prendre le premier)
                                    index = dist_eucl.tolist().index(dist_proche_voisin) #index de cette chaise dans la liste des distances euclidiennes
                                    prochaine_chaise = tableau_initial[index]  #désigner la prochaine chaise : sélectionner la proche chaise dans le array des chaises en jeu
                 
                        #plus loin voisin 
                        elif self.methode==3 and while_index>0 and sum(en_jeu)>1:  #si on est à la 2e boucle while 
                            voisins = dist_eucl[en_jeu] # retenir toutes les chaises à plus de la mesure de distanciation
    
                            if (min(voisins)==max(voisins)): #si aucun voisin ou si voisins min et max sont à la même distance #voisins.size==0 or 
                                prochaine_chaise = random.choice(tableau_initial[en_jeu]) #choisir au hasard
    
                            else:
                                dist_loin_voisin = max(voisins) #trouver voisin le plus loin (si il y en a deux, le premier)
                                index = dist_eucl.tolist().index(dist_loin_voisin) #index de cette chaise dans la liste des distances euclidiennes
                                prochaine_chaise = tableau_initial[index]  #désigner la prochaine chaise : sélectionner la proch. chaise dans le array des chaises en jeu
                
                        #plus proche voisin pondéré
                        elif self.methode==4 and while_index>0 and sum(en_jeu)>1:  #si si on est à la 2e boucle while 
                            #plus proche voisin pondéré 
                            voisins = dist_eucl[en_jeu] # retenir toutes les chaises à plus de 2m
                            
                            if voisins.size==0 or voisins.size==1 or (min(voisins)==max(voisins)):
                                prochaine_chaise = random.choice(tableau_initial[en_jeu])
                                         
                            else:
                                dist_loin_voisin = max(voisins)+0.1 
                                dist_proche_voisin = min(voisins)
                                ratios = ((dist_loin_voisin-voisins)/(dist_loin_voisin-dist_proche_voisin))/sum(((dist_loin_voisin-voisins)/(dist_loin_voisin-dist_proche_voisin)))
                                choix = random.choices(voisins, weights=ratios, k=1)[0]
                                index = dist_eucl.tolist().index(choix) #index de cette chaise dans la liste des distances euclidiennes
                                prochaine_chaise = tableau_initial[index]  #désigner la prochaine chaise : sélectionner la proch. chaise dans le array des chaises en jeu
                                
                        #plus loin voisin pondéré
                        elif self.methode==5 and while_index>0 and sum(en_jeu)>1:  #si on est à la 2e boucle while 
                            #plus loin voisin pondéré
                            voisins = dist_eucl[en_jeu] # retenir toutes les chaises à plus de 2m
                            
                            if voisins.size==0 or voisins.size==1 or (min(voisins)==max(voisins)):
                                prochaine_chaise = random.choice(tableau_initial[en_jeu])
                                         
                            else:
                                dist_loin_voisin = max(voisins)+0.1 
                                dist_proche_voisin = min(voisins)
                                ratios = ((voisins-dist_proche_voisin)/(dist_loin_voisin-dist_proche_voisin))/sum(((voisins-dist_proche_voisin)/(dist_loin_voisin-dist_proche_voisin)))
                                choix = random.choices(voisins, weights=ratios, k=1)[0]
                                index = dist_eucl.tolist().index(choix) #index de cette chaise dans la liste des distances euclidiennes
                                prochaine_chaise = tableau_initial[index]  #désigner la prochaine chaise : sélectionner la proch. chaise dans le array des chaises en jeu
                                    
                        #voisin aléatoire (méthode==1)          
                        else: 
                            #choisir chaise au hasard parmi celles en jeu
                            prochaine_chaise = random.choice(tableau_initial[en_jeu])
                        
                        prochaine_chaise[3]=1 #assigner occupation à 1 
                        couple = prochaine_chaise[1:3] #x et y de la chaise sélectionnée
                        dist_eucl = (tableau_initial[:,1:3] - couple)**2 #différence entre les x,y du couple et ceux de toutes les autres chaises
                        dist_eucl = dist_eucl.sum(axis=-1) #somme de la différence x,y
                        dist_eucl = np.sqrt(dist_eucl) #racine carrée de la différence
                        choisie = ((dist_eucl==0))#boolean chaise choisie
                        if hors_jeu.sum()>1: #s'il y a au moins 1 chaise hors jeu 
                            dist_eucl[hors_jeu] = np.zeros(hors_jeu.sum()) #dist. eucl. entre couple et chaises hors jeu = 0 
                        condition = ((dist_eucl<self.distance) & (dist_eucl>0)) #boolean chaises à <(distanciation)m et >0m
                        tableau_final[condition]=tableau_initial[condition] #déplacer ces chaises inadmissibles dans le deuxième tableau
                        tableau_final[choisie] = prochaine_chaise #ajouter chaise sélectionnée avec occupation=1 à l'array
                        tableau_initial[condition]=np.zeros(((condition.sum()),4)) #retirer chaises inadmissibles du array des chaises actives
                        tableau_initial[choisie]=np.zeros((1,4)) #retirer chaise choisie du array des chaises actives
                
                        while_index+=1
        
                #somme des chaises de cette itération
                somme_actuelle=tableau_final[:,3].sum()
                
                #si somme est meilleure que la meilleure somme jusqu'à présent dans les itérations précédente, assigner ce tableau comme meilleur tableau
                if somme_actuelle>meilleure_somme:
                    meilleure_somme=somme_actuelle
                    meilleur_tableau=tableau_final
                    
                #si on veut sortir les stats d'amélioration successive pour l'algo
                if self.analyse_perfo==True:
                    #ajouter num groupe, num itération, meilleur somme atteinte et methode
                    tableau_perfo.append([i,j, meilleure_somme,self.methode])
                    
                #early stopping with time
                time_now = time.time() #moment de fin de l'itération 
                potential_end = (time_now - start)/60 #temps écoulé en minutes depuis le début de l'algorithme
                       
                #si le temps actuel dépasse le temps maximum spécifié en paramètre, arrête
                if potential_end >= self.maximum_time:
                    break
            
            #sortir le meilleur tableau d'occupation pour ce sous-groupe de chaises
            return(meilleur_tableau) 

        resultat = []
        for i in nombre_groupes:
            sortie = calcul_groupe(i) 
            resultat.append(sortie)
            
        #concaténer les résultats de tous les groupes
        exclus_final=np.concatenate(resultat)       
        #trier par numéro de chaise en ordre croissant
        exclus_final = exclus_final[exclus_final[:, 0].argsort()]
        #calculer la capacité optimale finale de la salle regroupée
        capacite_optimale = exclus_final[:,3].sum()
        #créer array rempli de 0 avec 5 colonnes (pour ajouter numéro de groupe)
        array_final=np.zeros((len(donnees),5))
        #ajouter le choix final des chaises à ce nouvel array, array_final
        array_final[:,0:4]=exclus_final
        #ajouter le numéro de groupe en dernière colonne de l'array final
        array_final[:,4]=donnees[:,4]

        #convertir en liste
        meilleur_tableau = array_final.tolist() 
        
        #boucle pour ajouter l'orientation des chaises au tableau final
        for index, row in enumerate(meilleur_tableau):
            row.insert(1,orientations[index])
            
        #calculer temps écoulé pour tout l'algorithme
        end=time.time()
        total_time = (end - start)
        
        #indicateur d'interruption : voir si on dépassé le temps imparti
        potential_end = (end - start)/60
        if potential_end >= self.maximum_time:
            interrompu=1
        else:
            interrompu=0

        #entreposer les variables pour les réutiliser dans les méthodes suivantes
        self.total_time = total_time
        self.capacite_optimale = capacite_optimale
        self.interrompu = interrompu
        self.potential_end = (time.time())/60
        self.tableau_perfo = pd.DataFrame(tableau_perfo, columns=['Num_groupe','Num_iter','Best_somme_atteinte','Methode'])
        self.tableau_optimal=meilleur_tableau

        return meilleur_tableau,self.total_time
    
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
            print(f"L'algorithme a été interrompu à {self.potential_end} secondes") 

    #imprimer temps écoulé 
    def temps(self): 
        if len(self.tableau_optimal)==0: #si l'algorithme n'a pas roulé encore
            print("Vous devez d'abord utiiser rouler() pour lancer l'algorithme")
        else: #si on a roulé l'algorithme déjà, produire le temps écoulé
            print(f"Temps écoulé : {round(self.total_time,2)} secondes") 
        
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
            occup = pd.Categorical([row[4] for row in tableau], categories=[0,1], ordered=True)
            groups = pd.Categorical([row[5] for row in tableau], ordered=True)
            graphe = px.scatter(x=x_cord,y=y_cord,symbol=groups, color = occup, size = [1]*len(tableau), range_x=[0,max(x_cord)+1], range_y=[0,max(y_cord)+1]) 
            graphe.show()   