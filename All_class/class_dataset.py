import pathlib
import os
class dataset:
    def __init__(self):
        #Paths of the origin folder & the data folder, list of all files in the data folder
        self.folder = "\Data"
        self.path_origin = str(pathlib.Path(__file__).parent.parent.resolve())
        self.path_data = self.path_origin + self.folder
        self.data_files = os.listdir(self.path_data)
        self.data_selection = None

    def list_files(self):
        #Fonction that show all the files in the self.folder
        return self.data_files
    
    def data_selection_list(self, selection, transformation_int=False):
        #Fonction that create a list of all lines in the file, each line is a list
        #The transformation_int parameter is optional, if True, all the values will be transform in integer
        self.data_selection = selection
        data_list = []
        with open(self.path_data + "\\" + self.data_selection,"r") as f:
            f.readline() #Skip the 1st line (Header)
            for line in f:
                data_list.append(line.rstrip().split("\t"))
        if transformation_int == True:
            data_list = [[int(item) for item in chair] for chair in data_list]
        return data_list