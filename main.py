#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 15:44:38 2021

@author: equipe_algo
"""
import pathlib
import os

#Aller chercher dynamiquement le dossier Data et créer une liste des fichiers txt
path_origin = str(pathlib.Path(__file__).parent.resolve())
path_data = path_origin + "\Data"
data_files = os.listdir(path_data)
data_files_txt = []
for files in data_files:
    if files[-4:] == ".txt":
        data_files_txt.append(files)
print(data_files)
print(data_files_txt)

#Créer une liste de liste pour chaque source data
data_dict = {}
for files in data_files_txt:
    data_dict[files][0:-4] = 1
print(data_dict)
# for each in data_files_txt:
#     exec(f'data_{each} = []')
#     # list1 = []
#     # list2 = []
#     # list3 = []
# # with open('test.txt', 'r') as f:
# #     content = f.readlines()
# #     for x in content:
# #         row = x.split()
# #         list1.append(int(row[0]))
# #         list2.append(int(row[1]))
# #         list3.append(int(row[2]))


