#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 15:44:38 2021

@author: equipe_algo
"""
#On commence par créer une salle de cours rectangulaire


l=5 #longueur du rectangle
h=10 #hauteur du rectangle

m_longueur = list(range(1,l+1)) #un vecteur qui représente en mètres la position des chaises sur la longueur
m_hauteur = list(range(1,h+1)) #un vecteur qui représente en mètres la position des chaises sur la hauteur

#créer tous les couples de coordonnées x et y possibles
combinaisons = list(itertools.product(m_longueur,m_hauteur)) 


