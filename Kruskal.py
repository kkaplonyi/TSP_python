import numpy as np
import pandas as pd
import itertools as itr
import time
import scipy as sp
import scipy.sparse as csr_matrix


data1 = pd.read_excel('telepules_matrix.xls', index_col=0)
x0 = []#kezdeti megoldás
for i in data1:
    x0.append(i)
varos_szamlalo = data1.shape[0]
List_of_utak = list(itr.permutations(x0,2))
ut_sullyal = np.empty((0,3))
All_utak_sullyal = np.empty((0,3))
Counter_for_utak = 0
xz=[]
for i in List_of_utak:
    A_Counter = List_of_utak[Counter_for_utak] #megnézi az összes párt
    A_1 = A_Counter[0] #pár első fele
    A_2 = A_Counter[1] #pár második fele
    xz=np.append(xz,A_1)
    xz=np.append(xz,A_2)
    xsuly=data1.loc[xz[0],xz[1]]
    xz=xz[np.newaxis]
    ut_sullyal=np.column_stack((xsuly, xz))
    All_utak_sullyal=np.vstack((All_utak_sullyal,ut_sullyal))
    Counter_for_utak+=1
    xz=[]
    
All_utak_rendezve = np.array(sorted(All_utak_sullyal,key=lambda x: float(x[0])))
u=2
t=0
xFinal=[]
xFinal=np.append(xFinal, All_utak_rendezve[0,1])
xFinal=np.append(xFinal, All_utak_rendezve[0,2])


while u!=(varos_szamlalo):
    if All_utak_rendezve[t,2] in xFinal[:]:
        t+=1
    else:
        xFinal = np.append(xFinal, All_utak_rendezve[t,2])
        t+=1
        u+=1

###OF###
tavolsagok=[] #a célfüggvény részértékei
t=0
for i in range(len(xFinal)-1):
    x1=data1.loc[xFinal[t],xFinal[t+1]] # n és n+1 város
    x11 = data1.loc[xFinal[-1],xFinal[0]] #az utolsó és az első város   
    tavolsagok.append(x1)
    t=t+1


tavolsagok.append(x11) #hozzáadjuk az utolsó városból a kezdő városba való költséget (kör bezárása)
total_tav_kezdo=sum(tavolsagok) #tavolságok összeadása
print("Kruskal eredmenye: ",xFinal)
print("Total táv: ", total_tav_kezdo)

