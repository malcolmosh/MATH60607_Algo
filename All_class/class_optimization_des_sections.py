#first section: grouping seats into seperate sections with min 2 meter distance among all seats of one group with another
import pandas as pd
import time

class Optimization_des_sections():
    def __init__(self, data,distance,iterations=500, maximum_time=5):
        self.data = data
        self.distance = distance
        self.iterations = iterations
        self.maximum_time = maximum_time
    def optimize(self):
        time_start = time.time()
        #transformer en dataframe
        data_dataframe = pd.DataFrame(self.data,columns=("num","orient","pos_x","pos_y","use"))

        data_dataframe['group']=0
        data_dataframe['use']=0
        
        f=1 #group number holder
        print(data_dataframe)
        for n in range(0,len(data_dataframe.num)):#0 to 54
            if data_dataframe.group[n] ==0:
                data_dataframe.group[n]=f
                L=[n]
                merge = True
                while merge == True:
                    merge = False
                    for i in L:
                        for j in range(0,len(data_dataframe.num)):#0 to 54
                            if i != j and data_dataframe.group[j]==0 and ((((data_dataframe.pos_x[i]-data_dataframe.pos_x[j])**2)+((data_dataframe.pos_y[i]-data_dataframe.pos_y[j])**2))**0.5) < 2:
                                data_dataframe.group[j]=f
                                L.append(j)
                                merge = True
                f=f+1 
        #second section: finding use seats in each group/section & setting their availablity=1.
        #logic used here:
        #for each group we initialize a seat and add other seats based on their distance one by one.
        #we repeat above for all possible initial seats.
        #we choose the best result among different initial seats.
        group = data_dataframe['group'].unique() #geting list of all groups to use its size and select chaires per group
        for c in group: #for each group, we wanna create list use seats.
            s=[] #list of position of seats of group i
            for d in range(0,len(data_dataframe.num)):#we create list of position of seats in group i
                if data_dataframe.group[d]==c:
                    s.append(d)
            ss=[] #List of use seats in group i. we are going to enhance this list step by step
            for k in s:#we choose best selection among use seats in group i with initial seat k
                sss=[k] #adding first seat (initial seat k). 
                ddd=[k]
                add=True
                while add==True:#as far as we can add more seats as use
                    add=False
                    a=1000 #giving a big number to initial distance
                    t=-1 #initial position for 1st seat (k)
                    for q in s:#which seats in group i have min distance(and >= 2)meter from all seats already choosen
                        if q not in sss and q not in ddd:
                            m=1000 #giving a big number to initial distance
                            for p in sss:
                                dist=((((data_dataframe.pos_x[q]-data_dataframe.pos_x[p])**2)+((data_dataframe.pos_y[q]-data_dataframe.pos_y[p])**2))**0.5)
                                if dist != 0 and dist<m:
                                    m=dist #minimum distance of q from all p already in sss
                            if m<2:
                                ddd.append(q) 
                            elif m<a:
                                t=q
                                a=m
                    if t !=-1:
                        sss.append(t)
                        add=True
                if len(sss)>len(ss):
                    ss=sss
            for b in ss:
                data_dataframe.use[b]=1

        #transform to nested list
        nested_list = data_dataframe.values.tolist()
        time_end = time.time()
        time_total = time_end - time_start

        return nested_list, time_total







