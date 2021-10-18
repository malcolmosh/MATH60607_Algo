import pathlib
import os
class Dataset:
    def __init__(self):
        #Paths of the origin folder & the data folder, list of all files in the data folder
        self.folder = "Data"
        self.path_origin = str(pathlib.Path(__file__).parents[1].resolve())
        self.path_data = self.path_origin + "\\" + self.folder
        self.data_files = os.listdir(self.path_data)
        self.data_selection = None

    def list_files(self):
        #Fonction that show all the files in the self.folder
        return self.data_files
    
    def data_selection_list(self, selection):
        #Fonction that create a list of all lines in the file, each line is a list
        self.data_selection = selection
        data_list = []
        with open(self.path_data + "\\" + self.data_selection,"r") as f:
            f.readline() #Skip the 1st line (Header)
            for line in f:
                info = line.rstrip().split("\t")
                data_list.append([int(info[0]), float(info[1]), float(info[2]), bool(0)])
        return data_list