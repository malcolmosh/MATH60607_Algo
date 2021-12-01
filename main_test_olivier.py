#import random, pathlib, os, math, pygame
import pandas as pd
import numpy as np
import plotly.express as px

##test avec mes classes
from All_class.class_dataset import Salles
from All_class.class_voisins_exclus import Voisins_exclus

#importation données
test=Salles(app=False)
test.fichiers
mega="Salle Mega 1105.txt"
banque= "Salle Banque Scotia.txt"
cogeco = "Salle Cogeco.txt"
manuvie = "Salle Manuvie.txt"
saine = "Salle Saine Marketing.txt"
info, salle_classe = test.chairs_list_test(saine)


# algo olivier
optimize1=Voisins_exclus(salle_classe,distance=2, iterations=1000, methode=1, division=0)
tableau, temps = optimize1.optimize()
optimize1.resultat()
optimize1.graphe_sortie()
# tous_groupes = optimize1.tous_groupes
#
# optimize1.tableau_perfo
# optimize1.interruption()
# optimize1.graphe_entree()

# optimize1.temps()

#générer données 
def generer_donnees(salle, metaloops, distance, iterations, division):

    test=Salles(app=False)
    info, salle_classe = test.chairs_list_test(salle)

    meta_liste_2=[]
    for epoch in range(1,metaloops+1):
        meta_liste=[]
        #boucle méthodes
        for i in range(1,5):
            optimize1=Voisins_exclus(salle_classe,distance=distance,iterations=iterations,methode=i, division=division)
            optimize1.optimize()
            tous_groupes = [[epoch]+row for row in optimize1.tous_groupes]
            #tous_groupes=[row for row in tous_groupes]
            meta_liste.append(tous_groupes)
        meta_liste_2.append(meta_liste)
    
    #créer dataframe
    data_graphe = pd.DataFrame(np.concatenate(np.concatenate(meta_liste_2)),columns=['epoch', 'groupe', 'iteration','nb_chaises','methode_num'])
    #ajouter nom methode
    data_graphe['methode'] = data_graphe['methode_num'].map({1:"Voisin aléatoire",2:"Plus proche voisin",3:"Plus loin voisin",4:"Plus proche voisin pondéré"}) 
 
    #pour box plot 
    data_boite_moustache = data_graphe.groupby(["methode","epoch"], as_index=False).max()
    data_boite_moustache= data_boite_moustache.drop(columns=["groupe","iteration","methode_num"])
    data_graphe[data_graphe['nb_chaises']==13]

    #écraser les groupes au travers des epoch, methode et iterations
    data_graphe = data_graphe.groupby(["epoch","methode_num", "methode", "iteration"], as_index=False).sum()
    
    #remplacer le nombre de chaises dans chaque epoch, méthode et dans chaque groupe par le maximum, une fois qu'il est atteint
    data_np = np.array(data_graphe)
    for i in range (1,len(data_np)):
        if data_np[i,0]==data_np[i-1,0] and data_np[i,1]==data_np[i-1,1] and data_np[i,4]==data_np[i-1,4]:
            if data_np[i,5]<=data_np[i-1,5]:
                data_np[i,5]=data_np[i-1,5]

    #reconvertir en pandas
    data_graphe = pd.DataFrame(data_np, columns=data_graphe.columns)
    
    #moyenne au travers des méta-loops
    data_graphe= data_graphe.groupby(['methode','methode_num','groupe','iteration'],as_index=False).mean()
    data_graphe = data_graphe.drop(columns="epoch")
    data_graphe.reset_index(inplace=True)

    #max chaises
    max_chaises_atteint = data_graphe['nb_chaises'].max() 
    #trouver l'itération maximale à laquelle une des méthodes finit par converger à 100% (pour ajuster axes)
    derniere_iter_max = data_graphe[data_graphe['nb_chaises']==max_chaises_atteint].groupby("methode_num").first()['iteration'].max()
    
    # # #offset values by methode
    for i in range(1, len(data_graphe)):
        if data_graphe.loc[i,'methode_num']==2:
            data_graphe.loc[i,'nb_chaises']+=0.01
        elif data_graphe.loc[i,'methode_num']==3:
            data_graphe.loc[i,'nb_chaises']-=0.01
        elif data_graphe.loc[i,'methode_num']==4:
            data_graphe.loc[i,'nb_chaises']+=0.02
    
    #division
    if division==1:
        indicateur_div="Avec division"
    else:
        indicateur_div="Sans division"
        
    #titre salle
    if salle==mega:
        titre="Grande salle (1105 sièges)"
    elif salle==banque:
        titre="Salle Banque Scotia (70 sièges)"
    elif salle==cogeco:
        titre=="Salle Cogeco (31 sièges)"
    elif salle==manuvie:
        titre="Salle Manuvie (55 sièges)"
    elif salle==saine:
        titre="Salle Saine Marketing (56 sièges)"
        
    #details
    details="Dist. "+str(distance)+" m. "+indicateur_div+", "+str(metaloops)+" méta-itérations, "+str(iterations)+" itérations"

    return(titre, details, data_graphe, derniere_iter_max, data_boite_moustache)
            
def generer_graphe(titre, details, data, derniere_iter_max):
    config = {
      'toImageButtonOptions': {
        'format': 'png', # one of png, svg, jpeg, webp
        'filename': 'plot',
        'scale': 5 # Multiply title/legend/axis/canvas sizes by this factor
      }
    }

    #max chaises
    max_chaises_atteint = data_graphe['nb_chaises'].max() 
    
    #produire graphe
    graphe = px.line(data, x='iteration',y='nb_chaises', color="methode", 
                     labels=dict(iteration="Itération", nb_chaises="Capacité calculée", methode="Méthode"), 
                     title=titre+" - "+details)
    graphe.update_traces(mode="lines", line_shape="vh", line=dict(width=4))
    graphe.add_hline(y=max_chaises_atteint, line_dash="dot", annotation_text="Max. moyen atteint :"+str(round(max_chaises_atteint,2))+" chaises", annotation_position="top left", 
                     line_color="red")
    graphe.update_xaxes(range=[0,derniere_iter_max+10])
    graphe.show(config=config)   

def generer_boxplot(data):    
    #produire graphe boîte à moustache pour comparer le nombre de chaise atteint
    data2=data.groupby(["methode","nb_chaises"], as_index=False).count()
    data2['nb_chaises']=pd.Categorical(data2['nb_chaises'])
    fig = px.bar(data2,x="methode", y="epoch", color="nb_chaises",
                 title=titre+" - "+details,
                 labels=dict(epoch="Nombre de méta-itérations", nb_chaises="Capacité calculée", methode="Méthode"))
    fig.update_layout(barmode='group')
    fig.show()


#faire graphe 
titre, details, data_graphe, derniere_iter_max, data_boxplot = generer_donnees(salle=saine, metaloops=2, distance=2, iterations=10, division=0)

generer_graphe(titre=titre, details=details, data=data_graphe, derniere_iter_max=derniere_iter_max)

generer_boxplot(data=data_boxplot)

#graphe.update_yaxes()
#graphe.layout.yaxis2.matches = 'y2'


# #enlever groupes avec 1 chaise
# data_graphe.drop(data_graphe[data_graphe["nb_chaises"]==1].index, inplace=True)
# data_graphe.reset_index(inplace=True)

# #offset values by methode
# for i in range(1, len(data_graphe)):
#     if data_graphe.loc[i,'methode_num']==2:
#         data_graphe.loc[i,'nb_chaises']+=0.05
#     elif data_graphe.loc[i,'methode_num']==3:
#         data_graphe.loc[i,'nb_chaises']+=0.10
#     elif data_graphe.loc[i,'methode_num']==4:
#         data_graphe.loc[i,'nb_chaises']+=0.15   



#graphe 2
graphe = px.line(data_graphe, x='iteration',y='nb_chaises', facet_row = 'groupe', facet_col="methode", color='methode')
# graphe.update_yaxes()
graphe.layout.yaxis2.matches = 'y2'
graphe.layout.yaxis6.matches = 'y5'
graphe.layout.yaxis7.matches = 'y5'
graphe.layout.yaxis8.matches = 'y5'
graphe.show()   


#tester avec manuvie, avec grande salle rectangulaire, avec grande salle qui a des division


#creer salle classe grand carré (500 places)
test=[]

for i in range(1,20):
    for j in range(1,10):
        a=[i,"south",i,j,False]
        test.append(a)

for i in range(1,len(salle_classe)):
    test[i][0]=i+1
salle_classe=test