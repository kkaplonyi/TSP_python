import numpy as np
import pandas as pd
import itertools as itr
import Kruskal
import OF
from datetime import datetime
#import mysql.connector

#conn = mysql.connector.connect(host='192.168.1.70', database='tsp', user='kkaplonyi', password='TSP123abc')
#cursor = conn.cursor()
#print("Connection Succesfull!")

def alg(M_raw, T_length_raw):
    
    
    x0 = Kruskal.xFinal
    
    ###PARAMÉTEREK###
    M = M_raw #max iterációszám
    Tabu_length = T_length_raw #tabulista mérete
    Tabu_length_0=Tabu_length
    Tabu_list = np.empty((0, len(x0)+1)) #a tabulista és +1 oszlop hogy a fitness értéket is tároljuk
    xFinal=[] #végső megoldás
    iterations =1
    Megoldas_gyujto=np.empty((0, len(x0)+1))

    for i in range(M):        
        ###Az összes szomszéd létrehozása###
        List_of_N = list(itr.combinations(x0,2)) #a 2-optal az összes kombináció

        Counter_for_N= 0 #iteráció számláló
        All_N_for_i= np.empty((0,len(x0)))
        for i in List_of_N:
            x_swap=[]
            A_Counter = List_of_N[Counter_for_N] #megnézi az összes párt
            A_1 = A_Counter[0] #pár első fele
            A_2 = A_Counter[1] #pár második fele

            ###megcserélés###
            u=0
            for j in x0:
                if x0[u]==A_1:
                    x_swap = np.append(x_swap,A_2)
                elif x0[u]==A_2:
                    x_swap = np.append(x_swap,A_1)
                else:
                    x_swap=np.append(x_swap,x0[u])

                x_swap = x_swap[np.newaxis]

                u +=1
            All_N_for_i = np.vstack((All_N_for_i,x_swap))
            Counter_for_N+=1

        OF_value_for_Ni = np.empty((0,len(x0)+1)) #aktuális kiegészítve OF-vel
        OF_value_for_All_N = np.empty((0,len(x0)+1)) #stackelt kiegészítve OF-vel

        N_Count = 1
        for i in All_N_for_i:
            xtemp = i
            total_tav_temp=OF.OF_cal(xtemp) #tavolságok összeadása
            i=i[np.newaxis]
            OF_value_for_Ni = np.column_stack((total_tav_temp,i))
            OF_value_for_All_N = np.vstack((OF_value_for_All_N,OF_value_for_Ni))
            
            N_Count+=1

        OF_mindenes_rendezve = np.array(sorted(OF_value_for_All_N,key=lambda x: float(x[0]))) #sorba rendezés fitness érték alapján

        t=0
        Current_Sol = OF_mindenes_rendezve[t]

        ###Tabu-lista ellenőrzés###
        while Current_Sol[0] in Tabu_list[:,0]:
            Current_Sol = OF_mindenes_rendezve[t]
            t+=1

        if len(Tabu_list)>= Tabu_length: #Tabu lista teli
            Tabu_list = np.delete(Tabu_list, (Tabu_length-1), axis = 0) #utolso sor törlése

        Tabu_list = np.vstack((Current_Sol, Tabu_list))

        Megoldas_gyujto = np.vstack((Current_Sol, Megoldas_gyujto))


        ###Továbblépés tabu módra###
        Mod_iterations = iterations%10
        ran_1 = np.random.randint(1, len(x0)+1)
        ran_2 = np.random.randint(1, len(x0)+1)
        ran_3 = np.random.randint(1, len(x0)+1)

        if Mod_iterations ==0:
            xt = []
            a1 = Current_Sol[ran_1]
            a2 = Current_Sol[ran_2]


            s_temp = Current_Sol

            w=0
            for i in s_temp:
                if s_temp[w]==a1:
                    xt=np.append(xt, a2)
                elif s_temp[w]==a2:
                    xt=np.append(xt, a1)
                else:
                    xt = np.append(xt, s_temp[w])
                w+=1

            Current_Sol = xt

            xt = []
            a1 = Current_Sol[ran_1]
            a2 = Current_Sol[ran_3]

            w=0
            for i in s_temp:
                if s_temp[w]==a1:
                    xt=np.append(xt, a2)
                elif s_temp[w]==a2:
                    xt=np.append(xt, a1)
                else:
                    xt = np.append(xt, s_temp[w])
                w+=1

            Current_Sol = xt

        x0=Current_Sol[1:]

        iterations+=1

        if Mod_iterations == 5 or Mod_iterations==0:
            Tabu_length = np.random.randint(5,20)

    t=0
    Final_here = []
    for i in Megoldas_gyujto:
        if Megoldas_gyujto[t,0]<=min(Megoldas_gyujto[:,0]):
            Final_here = Megoldas_gyujto[t,:]
        t+=1    

    xFinal=Final_here[1:20]
    XFinal_of = float(Final_here[0])
    current_Date = datetime.now()
    formatted_date = current_Date.strftime('%Y-%m-%d')
    #SQLCommand="""INSERT INTO tsp.tabu(run_time, OFV, M, T_length) VALUES(%s,%s,%s,%s)"""
    #Values = [formatted_date, float(XFinal_of), int(M), int(Tabu_length_0)]
    #cursor.execute(SQLCommand, Values)
    #conn.commit()
    export = [] 
    export.append(formatted_date)
    export.append(float(XFinal_of))
    export.append(int(M))
    export.append(int(Tabu_length_0))
    print("Tabu Siker!")
    return export
