import pathlib
import os

class Salles: #nouvelle classe
    def __init__(self, folder_data="Data",app=True): 
        self.app = app
        if self.app == False:
            #Paths of the origin folder & the data folder, list of all files in the data folder
            self.folder_data = folder_data #nom dossier
            self.path_origin = str(pathlib.Path(__file__).parents[1].resolve()) #chemin d'accès repo
            self.path_data = os.path.join(self.path_origin,self.folder_data) #chemin d'accès dossier data
            self.data_files = os.listdir(self.path_data) #fichiers dans le dossier data
            self.fichiers = (f"Fichiers présents dans le dossier: {self.data_files}")
        elif self.app == True:
            pass

    def chairs_list(self, selection):
        self.selection= selection #nom dossier
        #Créer une liste à partir du fichier sélection : chaque ligne est une liste 
        data_chair = []
        with open(self.selection,"r") as f:
            f.readline() #Skip the 1st line (Header of info)
            line = f.readline()
            data = line.rstrip().split("\t")
            data_info = {"width":float(data[0]), "height":float(data[1])}
            
        with open(self.selection,"r") as f:
            f.readline() #Skip the 1st line (Header of info)
            f.readline() #Skip the 2nd line (Info)
            f.readline() #Skip the 3rd line (Header)
            for line in f:
                info = line.rstrip().split("\t")
                data_chair.append([int(info[0]), str(info[1]), float(info[2]), float(info[3]),bool(0)])

        return data_info,data_chair
    
    def chairs_list_test(self, selection):
        self.selection= selection #nom dossier
    #Créer une liste à partir du fichier sélection : chaque ligne est une liste 
        data_chair = []
        with open(os.path.join(self.path_data,self.selection),"r") as f:
            f.readline() #Skip the 1st line (Header of info)
            line = f.readline()
            data = line.rstrip().split("\t")
            data_info = {"width":float(data[0]), "height":float(data[1])}
            
        with open(os.path.join(self.path_data,self.selection),"r") as f:
            f.readline() #Skip the 1st line (Header of info)
            f.readline() #Skip the 2nd line (Info)
            f.readline() #Skip the 3rd line (Header)
            for line in f:
                info = line.rstrip().split("\t")
                data_chair.append([int(info[0]), str(info[1]), float(info[2]), float(info[3]),bool(0)])

        return data_info,data_chair
