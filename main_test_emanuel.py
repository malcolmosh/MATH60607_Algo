from All_class.class_dataset import dataset
import random
import pygame

def optimization(data_list):
    for chair in range(0,len(data_list)):
        data_list[chair].append(random.randint(0,1))
        
data = dataset()
print(data.list_files())
data_selection = data.data_selection_list("salle_test50.txt",True)
print(data_selection)

optimization(data_selection)
print(data_selection)
