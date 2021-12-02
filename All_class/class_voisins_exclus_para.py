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
    
    def __init__(self, data,distance,iterations=500, maximum_time=5, methode=1, division=0):
        self.data = data
        self.distance = distance
        self.iterations = iterations
        self.maximum_time = maximum_time
        self.methode=methode
        self.division = division
        self.tableau_optimal=()
        
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
        
        #boucle pour chaque groupe
        def calcul_groupe(i):
            
            #tableau d'occupation des chaises du groupe i
            resultat_iterations=[]
            #nombre de chaises du groupe i
            somme_iterations=[] 
            #entreposer toutes les configurations de chaque itération pour tous les groupes
            tous_groupes=[]


            for j in range(self.iterations): 
                

                #sélectionner les chaises de ce groupe
                subset = donnees[np.where(donnees[:,4] ==i)]
                chaises=subset[:,0:4].copy() #initialiser array chaises 
                exclus=np.zeros((len(chaises),4)) #initialiser liste vide exclus
            
                while_index = 0 #index des boucles du while
            
                while (chaises[:,1:4].sum()>0): #pendant qu'il y a encore des chaises encore en jeu 
                    en_jeu= (chaises[:,1:4].sum(axis=-1)>0) #boolean chaises qui sont en jeu
                    hors_jeu = (chaises[:,1:4].sum(axis=-1)==0) #boolean chaises qui ne sont plus en jeu
                    
                    #sélection prochaine chaise : 
                        #methode == 1 : au hasard
                        #methode == 2 : plus proche voisin
                        #methode == 3 : plus loin voisin
                        #methode ==4 : weighed random avec pourcentage
                        
                    if len(subset)==1: #si qu'une chaise dans ce groupe
                        subset[0,3]=1 #assigner chaise occupée à la seule chaise dispo pour cette itération
                        exclus=subset[:,0:4]
                        chaises[0:4]=[0,0,0,0]
                        
                    else:
                        
                        if self.methode==2 and while_index>0 and sum(en_jeu)>1:  #si algorithme plus proche voisin est choisi et si on est à la 2e boucle while 
                            #trouver plus proche voisin admissible
                            voisins = dist_eucl[en_jeu] # retenir toutes les chaises à plus de la distance spécifiée 
     
                            if (min(voisins)==max(voisins)): #si voisins min et max sont à la même distance
                                prochaine_chaise = random.choice(chaises[en_jeu]) #choisir au hasard 
    
                            else:                  
                                dist_proche_voisin = min(voisins) #trouver voisin le plus proche (si il y en a deux, prendre le premier)
                                index = dist_eucl.tolist().index(dist_proche_voisin) #index de cette chaise dans la liste des distances euclidiennes
                                prochaine_chaise = chaises[index]  #désigner la prochaine chaise : sélectionner la proche chaise dans le array des chaises en jeu
                 
                        elif self.methode==3 and while_index>0 and sum(en_jeu)>1:  #si algorithme plus loin voisin est choisi et si on est à la 2e boucle while 
                            #trouver plus loin voisin admissible
                            voisins = dist_eucl[en_jeu] # retenir toutes les chaises à plus de la mesure de distanciation
    
                            if (min(voisins)==max(voisins)): #si aucun voisin ou si voisins min et max sont à la même distance #voisins.size==0 or 
                                prochaine_chaise = random.choice(chaises[en_jeu]) #choisir au hasard
    
                            else:
                                dist_loin_voisin = max(voisins) #trouver voisin le plus loin (si il y en a deux, le premier)
                                index = dist_eucl.tolist().index(dist_loin_voisin) #index de cette chaise dans la liste des distances euclidiennes
                                prochaine_chaise = chaises[index]  #désigner la prochaine chaise : sélectionner la proch. chaise dans le array des chaises en jeu
                
                        elif self.methode==4 and while_index>0 and sum(en_jeu)>1:  #si algorithme voisin pondéré est choisi et si on est à la 2e boucle while 
                            #trouver prochain voisin admissible avec une probabilité pondérée 
                            voisins = dist_eucl[en_jeu] # retenir toutes les chaises à plus de la mesure de distanciation
    
                            if (min(voisins)==max(voisins)): #si voisins min et max sont à la même distance
                                prochaine_chaise = random.choice(chaises[en_jeu]) #prendre la prochaine chaise au hasard
    
                            else:
                                dist_loin_voisin = max(voisins) #trouver voisin le plus loin (si il y en a deux, le premier)
                                ratios =(1-(voisins/dist_loin_voisin))/(sum(1-(voisins/dist_loin_voisin))) #construire un ratio de distances
                                choix = random.choices(voisins, weights=ratios, k=1)[0] #choisir au hasard avec ces poids de ratio 
                                index = dist_eucl.tolist().index(choix) #index de cette chaise dans la liste des distances euclidiennes
                                prochaine_chaise = chaises[index]  #désigner la prochaine chaise : sélectionner la proch. chaise dans le array des chaises en jeu
    
                        else: #méthode==1
                            prochaine_chaise = random.choice(chaises[en_jeu]) #choisir chaise au hasard parmi celles en jeu
                        
                        prochaine_chaise[3]=1 #assigner occupation à 1 
                        couple = prochaine_chaise[1:3] #x et y de la chaise sélectionnée
                        dist_eucl = (chaises[:,1:3] - couple)**2 #différence entre les x,y du couple et ceux de toutes les autres chaises
                        dist_eucl = dist_eucl.sum(axis=-1) #somme de la différence x,y
                        dist_eucl = np.sqrt(dist_eucl) #racine carrée de la différence
                        choisie = ((dist_eucl==0))#boolean chaise choisie
                        if hors_jeu.sum()>1: #s'il y a au moins 1 chaise hors jeu 
                            dist_eucl[hors_jeu] = np.zeros(hors_jeu.sum()) #dist. eucl. entre couple et chaises hors jeu = 0 
                        condition = ((dist_eucl<self.distance) & (dist_eucl>0)) #boolean chaises à <(distanciation)m et >0m
                        exclus[condition]=chaises[condition] #ajouter ces chaises trop proche aux exclus
                        exclus[choisie] = prochaine_chaise #ajouter chaise sélectionnée avec occupee=1 à l'array
                        chaises[condition]=np.zeros(((condition.sum()),4)) #retirer couples exclus du array des chaises actives
                        chaises[choisie]=np.zeros((1,4)) #retirer chaise choisie du array des chaises actives
                
                        while_index+=1
            
                #ajouter la configuration des chaises de cette itération
                resultat_iterations.append(exclus)
                #ajouter la somme des chaises occupées
                somme_iterations.append(exclus[:,3].sum())
                #ajouter le # de groupe, le # de l'itération et la somme des chaises occupées
                tous_groupes.append([i,j,exclus[:,3].sum(),self.methode])
                #early stopping with time
                time_now = time.time() #moment de fin de l'itération 
                       
                #si le temps dépasse le temps maximum fourni en paramètre, arrêter à la fin de l'itération
                if (time_now - start)/60 >= self.maximum_time:
                    interrompu=1
                    break
                else:
                    interrompu=0

            capacite_opt_groupe=max(somme_iterations) #capacité optimale trouvée pour ce groupe
            index_best=somme_iterations.index(capacite_opt_groupe) #index de cette meilleure itération
            meilleur_subset=resultat_iterations[index_best] #retenir tableau optimal à cet index           
            nombre_chaises = len(meilleur_subset) #nombre de chaises de ce sous-groupe
            return([[i,nombre_chaises,index_best], meilleur_subset,tous_groupes, interrompu]) #sortir tableau perfo, meilleur tableau, tous les tableaux de toutes les itérations pour ce groupe, avis d'interruption
        
        #rouler tâches en parallèle
        from joblib import Parallel, delayed
        import multiprocessing

        num_cores = multiprocessing.cpu_count()
        resultat = Parallel(n_jobs=num_cores)(delayed(calcul_groupe)(i) for i in nombre_groupes)

        #liste pour entrepose le numero de groupe, le nombre de chaises et l'index de l'itération avec le meilleur résultat
        tableau_perfo=[item[0] for item in resultat]
        #liste pour la meilleure configuration de chaque groupe (concaténer les résultats ensemble)
        exclus_final=np.concatenate([item[1] for item in resultat])
        #cette liste sert à évaluer la performance de la méthode choisie
        tous_groupes=[item[2] for item in resultat]
        tous_groupes=[item for sublist in tous_groupes for item in sublist]
        #interruptions
        interrompu=sum([item[3] for item in resultat])
        #trier par numéro de chaise en ordre croissant
        exclus_final = exclus_final[exclus_final[:, 0].argsort()]
        #calculer la capacité optimale finale de la salle
        capacite_optimale = exclus_final[:,3].sum()
        #créer array rempli de 0 avec 5 colonnes
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

        #entreposer les variables pour les réutiliser dans les méthodes suivantes
        self.total_time = total_time
        self.capacite_optimale = capacite_optimale
        self.interrompu = interrompu
        self.potential_end = (time.time())/60
        self.tableau_perfo = pd.DataFrame(tableau_perfo, columns=['Num_groupe','Nombre chaises','Iteration_best'])
        self.tous_groupes = tous_groupes
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