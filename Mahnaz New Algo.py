#first section: grouping seats into seperate sections with min 2 meter distance among all seats of one group with another
import pandas as pd
data=pd.read_csv("Salle Saine Marketing 1 meter dist.csv")
data['group']=0
data['available']=0
f=1 #group number holder
for n in range(0,len(data.num)):#0 to 54
    if data.group[n] ==0:
        data.group[n]=f
        L=[n]
        merge = True
        while merge == True:
            merge = False
            for i in L:
                for j in range(0,len(data.num)):#0 to 54
                    if i != j and data.group[j]==0 and ((((data.pos_x[i]-data.pos_x[j])**2)+((data.pos_y[i]-data.pos_y[j])**2))**0.5) < 2:
                        data.group[j]=f
                        L.append(j)
                        merge = True
        f=f+1   
#second section: finding available seats in each group/section & setting their availablity=1.
#logic used here:
#for each group we initialize a seat and add other seats based on their distance one by one.
#we repeat above for all possible initial seats.
#we choose the best result among different initial seats.
group = data['group'].unique() #geting list of all groups to use its size and select chaires per group
for c in group: #for each group, we wanna create list available seats.
    s=[] #list of position of seats of group i
    for d in range(0,len(data.num)):#we create list of position of seats in group i
        if data.group[d]==c:
            s.append(d)
    ss=[] #List of available seats in group i. we are going to enhance this list step by step
    for k in s:#we choose best selection among available seats in group i with initial seat k
        sss=[k] #adding first seat (initial seat k). 
        ddd=[k]
        add=True
        while add==True:#as far as we can add more seats as available
            add=False
            a=1000 #giving a big number to initial distance
            t=-1 #initial position for 1st seat (k)
            for q in s:#which seats in group i have min distance(and >= 2)meter from all seats already choosen
                if q not in sss and q not in ddd:
                    m=1000 #giving a big number to initial distance
                    for p in sss:
                        dist=((((data.pos_x[q]-data.pos_x[p])**2)+((data.pos_y[q]-data.pos_y[p])**2))**0.5)
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
        data.available[b]=1
print(data)