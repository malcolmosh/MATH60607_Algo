from All_class.class_dataset import Salles
from All_class.class_optimization_random import Optimization_random
from All_class.class_application_tkinter import Application
import random, pathlib, os, pygame, math
from sys import exit

data = Salles()
# print(data.list_files())
# data_selection = data.chairs_list("Salle Saine Marketing.txt")
# print(data_selection)
# room_info = data.room_info("Salle Saine Marketing Info.txt")
# # #print(room_info)
# optimization = Optimization_random(data_selection)
# optimization_export = optimization.optimize(25)
# for chair in optimization_export:
#     print(chair)


app = Application()