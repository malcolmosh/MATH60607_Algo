import pathlib
import os
class Dataset:
    def __init__(self):
        #Paths of the origin folder & the data folder, list of all files in the data folder
        self.folder = "Data" #nom dossier
        self.path_origin = str(pathlib.Path(__file__).parents[1].resolve()) #chemin d'accès repo
        self.path_data = os.path.join(self.path_origin,self.folder) #chemin d'accès dossier data
        self.data_files = os.listdir(self.path_data) #fichiers dans le dossier data

    def list_files(self):
        #Retourner touxs les fichiers dans le self.folder
        data_files = self.data_files 
        print(f"Fichiers présents dans le dossier Data: {data_files}") 
    
    def chairs_list(self, selection):
        #Créer une liste à partir du fichier sélection : chaque ligne est une liste 
        self.data_selection = selection
        data_list = []
        with open(os.path.join(self.path_data,self.data_selection),"r") as f:
            f.readline() #Skip the 1st line (Header)
            for line in f:
                info = line.rstrip().split("\t")
                data_list.append([int(info[0]), float(info[1]), float(info[2]), bool(0)])
        return data_list

    def room_info(self, selection):
        self.room_selection = selection
        room_list = []
        with open(os.path.join(self.path_data,self.room_selection),"r") as f:
            f.readline() #Skip the 1st line (Header)
            for line in f:
                info = line.rstrip().split("\t")
                room_list.append(float(info[0]))
                room_list.append(float(info[1]))
        return room_list