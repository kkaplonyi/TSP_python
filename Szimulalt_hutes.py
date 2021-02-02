import numpy as np
import pandas as pd
import time
import Kruskal
import OF
from datetime import datetime
#import mysql.connector

#conn = mysql.connector.connect(host='192.168.1.70', database='tsp', user='kkaplonyi', password='TSP123abc')
#cursor = conn.cursor()

def alg(T0_raw, M_raw, N_raw, alpha_raw):

    # Importálás specificikus directoryból
    #data1 = pd.read_excel ('telepules_matrix.xls', index_col=0)
    #print(data1)
    x0 = Kruskal.xFinal


    #print(x0)


    ###OF###
    #total_tav_kezdo=OF.OF_cal(x0) 
    #print("Total táv: ", total_tav_kezdo)

    ###PARAMÉTEREZÉS###

    T0 =T0_raw  #kezdeti hőmérséklet
    T0_0=T0
    M=M_raw #mutáció száma
    N=N_raw #szomszédok száma
    alpha=alpha_raw #hűtési ráta (0.85)


    ###algoritmus###
    Temp=[] #gyujto
    min_tav=[] #gyujto

    for i in range(M):
        for j in range(N):
            #két random szám generálása a városok felcseréléséhez
            ran1 = np.random.randint(0,len(x0))
            ran2 = np.random.randint(0,len(x0))
            while ran1==ran2:
                ran2 = np.random.randint(0,len(x0))

            xtemp =[]
            a1=x0[ran1] #1. a random által választott város
            a2=x0[ran2] #2. a random által választott város

            #a csere
            w=0
            for i in x0:
                if x0[w]==a1:
                    xtemp=np.append(xtemp,a2)
                elif x0[w]==a2:
                    xtemp=np.append(xtemp,a1)
                else:
                    xtemp=np.append(xtemp, x0[w])
                w+=1
            xtemp =list(xtemp) #ideiglenes megoldás

            total_tav_x0=OF.OF_cal(x0) #tavolságok összeadása

            total_tav_temp=OF.OF_cal(xtemp) #tavolságok összeadása

            rand_num = np.random.rand() #uj random változó a továbblépési formulához
            form_1 = np.exp((-total_tav_temp+total_tav_x0)/T0) #továbblépési formula

            if total_tav_temp<=total_tav_x0: #az új jobb mint a megeleőző
                x0=xtemp

            elif rand_num<=form_1: #az új nem jobb, de a a random kisebb a formulánál így megtartjuk
                x0=xtemp

            else: #nem jobb és nem is fogadjuk el
                x0=x0

        Temp = np.append(Temp, T0)
        min_tav = np.append(min_tav,total_tav_temp)

        T0=alpha*T0 #hőmérséklet csökkentése 

    current_Date = datetime.now()
    formatted_date = current_Date.strftime('%Y-%m-%d')
    #SQLCommand="""INSERT INTO tsp.sz_hutes(run_time, OFV, T0, M, N, alpha) VALUES(%s,%s,%s,%s,%s,%s)"""
    #Values = [formatted_date, float(total_tav_x0), float(T0_0), int(M), int(N), float(alpha)]
    #cursor.execute(SQLCommand, Values)
    #conn.commit()
    export = [] 
    export.append(formatted_date)
    export.append(float(total_tav_x0))
    export.append(float(T0_0))
    export.append(int(M))
    export.append(int(N))
    export.append(float(alpha))
    print("SZA Siker!")
    return export
    """print
    print
    print("A végső emgoldás: ", x0)
    print("A minimum út a végső megoldásban: ", total_tav_x0)"""
