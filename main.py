from All_class.class_dataset import Dataset
from All_class.class_game import Game
import random, pathlib, os, pygame, math
from sys import exit


data = Dataset()
print(data.list_files())
data_selection = data.data_selection_list("salle_test50.txt")
for chair in data_selection:
    print(chair)

optimization = 
# optimization(data_selection)
# print(data_selection)




# g = Game()

# while g.running:
#     g.curr_menu.display_menu()
#     g.game_loop()