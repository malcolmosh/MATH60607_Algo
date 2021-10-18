from All_class.class_dataset import Dataset
from All_class.class_optimization_random import Optimization_random
from All_class.class_application import Application
import random, pathlib, os, pygame, math
from sys import exit

data = Dataset()
# print(data.list_files())
data_selection = data.chairs_list("salle_test108.txt")
# for chair in data_selection:
#     print(chair)
room_info = data.room_info("salle_test108_info.txt")
#print(room_info)
optimization = Optimization_random(data_selection)
optimization_export = optimization.optimize(25)
# for chair in optimization_export:
#     print(chair)


app = Application(optimization_export, room_info)
app.game_loop()