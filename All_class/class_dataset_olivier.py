
import pathlib
import os

class Salles: #nouvelle classe
    def __init__(self, folder_data="Data"): 
        #Paths of the origin folder & the data folder, list of all files in the data folder
        self.folder_data = folder_data #nom dossier
        self.path_origin = str(pathlib.Path(__file__).parents[1].resolve()) #chemin d'accès repo
        self.path_data = os.path.join(self.path_origin,self.folder_data) #chemin d'accès dossier data
        self.data_files = os.listdir(self.path_data) #fichiers dans le dossier data
        
    def __str__(self):
        return(f"Fichiers présents dans le dossier: {self.data_files}") 

    def chairs_list(self, selection):
        self.selection= selection #nom dossier

    #Créer une liste à partir du fichier sélection : chaque ligne est une liste 
        data_list = []
        with open(os.path.join(self.path_data,self.selection),"r") as f:
            f.readline() #Skip the 1st line (Header)
            for line in f:
                info = line.rstrip().split("\t")
                data_list.append([int(info[0]), float(info[1]), float(info[2]), bool(0)])
        return data_list
     