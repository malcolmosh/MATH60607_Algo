import pathlib
import os

class Dataset:
    def __init__(self, Data):
        #Paths of the origin folder & the data folder, list of all files in the data folder
        self.folder = Data #nom dossier
        self.path_origin = str(pathlib.Path(__file__).parents[1].resolve()) #chemin d'accès repo
        self.path_data = os.path.join(self.path_origin,self.folder) #chemin d'accès dossier data
        self.data_files = os.listdir(self.path_data) #fichiers dans le dossier data

    def __str__(self):
        return(f"Fichiers présents dans le dossier Data: {self.data_files}") 

import numpy as np
import random #sélection aléatoire

class salle(Dataset): #sous-classe de dataset qui s'appelle salle
    def __init__(self, data, selection): 
        super().__init__(data)
        self.data = data
        self.selection = selection
        
    def __str__(self):
        return(f"Nom de la salle de classe: {self.selection}") 

    def chairs_list(self):
    #Créer une liste à partir du fichier sélection : chaque ligne est une liste 
        data_list = []
        with open(os.path.join(self.path_data,self.selection),"r") as f:
            f.readline() #Skip the 1st line (Header)
            for line in f:
                info = line.rstrip().split("\t")
                data_list.append([int(info[0]), float(info[1]), float(info[2]), bool(0)])
        return data_list
    
    def room_info(self):
        room_list = []
        with open(os.path.join(self.path_data,self.selection),"r") as f:
            f.readline() #Skip the 1st line (Header)
            for line in f:
                info = line.rstrip().split("\t")
                room_list.append(float(info[0]))
                room_list.append(float(info[1]))
        return room_list
    
    def algo1(self,iterations,distanciation):    
        data=self.chairs_list() #importer données 
        data=np.array(data) #convertir fichier données en array
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
      
import plotly.io as pio
import plotly.express as px
pio.renderers.default='browser' #pour générer graphiques plotly dans browser
import pandas as pd

class algo1:
    
    def __init__(self, data,distance,iterations=500):
        self.data=data
        self.iterations=iterations
        self.distance=distance
        self.tableau_optimal=() #vecteur qui contiendra la meilleure sortie de l'algorithme
        
    #vérifier si les listes du début sont vides ou pas
    #voir https://stackoverflow.com/questions/32836291/check-if-object-attributes-are-non-empty-python
    def __nonzero__(self): 
        return bool(self.tableau_optimal)
    
    #rouler l'algorithme
    def rouler(self):    
        data=np.array(self.data) #convertir fichier données en array
        liste_capacite=[] #liste vide pour contenir nombre de chaises retenu par itération 
        list_tableaux=[] #liste vide qui contiendra le array final par itération
         
        for i in range(self.iterations): #répéter un grande nombre de fois
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
                condition = ((dist_eucl<self.distance) & (dist_eucl>0)) #boolean chaises à <(distanciation)m et >0m
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
        meilleure_iteration=liste_capacite.index(capacite_optimale) #meilleure itération parmi le loop
        meilleur_tableau=list_tableaux[meilleure_iteration] #tableau des groupes de la meilleure itération
        self.tableau_optimal=meilleur_tableau
        print(f"La capacité optimale de la salle est de {capacite_optimale:.0f} places") #print capacité optimale
    
    #array de la meilleure itération
    def tableau(self): 
        if len(self.tableau_optimal)==0: #si l'algorithme n'a pas roulé encore
            print("Vous devez d'abord utiiser rouler() pour lancer l'algorithme")
        else: #si on a roulé l'algorithme déjà, produire la meilleure sortie
            return(self.tableau_optimal)
        
    #graphe initial de la salle
    def graphe_entree(self): 
        if len(self.tableau_optimal)==0: #si l'algorithme n'a pas roulé encore
            print("Vous devez d'abord utiiser rouler() pour lancer l'algorithme")
        else: #si on a roulé l'algorithme déjà, sortir le graphique initial
            graphe = px.scatter(x=self.tableau_optimal[:,1],y=self.tableau_optimal[:,2], size=([1]*len(self.tableau_optimal)),range_x=[0,max(self.tableau_optimal[:,1])+1], range_y=[0,max(self.tableau_optimal[:,2])+1]) 
            graphe.show()
            
    #graphe final de la salle
    def graphe_sortie(self): 
        if len(self.tableau_optimal)==0: #si l'algorithme n'a pas roulé encore
            print("Vous devez d'abord utiiser rouler() pour lancer l'algorithme")
        else: #si on a roulé l'algorithme déjà, sortir le graphique final
            groups = pd.Categorical(self.tableau_optimal[:,3], categories=[0,1], ordered=True)
            graphe = px.scatter(x=self.tableau_optimal[:,1],y=self.tableau_optimal[:,2], color=groups, size=([1]*len(self.tableau_optimal)),range_x=[0,max(self.tableau_optimal[:,1])+1], range_y=[0,max(self.tableau_optimal[:,2])+1]) 
            graphe.show()
        
    #a ajouter
    #couples= meilleur_tableau[meilleur_tableau[:,3]==1] #lignes des chaises sélectionnées
    #chaises_choises=list(couples[:,0]) #numéros de chaise sélectionnés

       