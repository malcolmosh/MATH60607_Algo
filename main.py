import pathlib
import os
from All_class.class_dataset import dataset

data = dataset()
data_selection = data.data_selection_list("salle_test50.txt",True)
print(data_selection)


