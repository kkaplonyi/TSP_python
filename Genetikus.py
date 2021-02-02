import numpy as np
import pandas as pd
import random as rd
import Kruskal
import OF
from datetime import datetime
#import mysql.connector

#conn = mysql.connector.connect(host='192.168.1.70', database='tsp', user='kkaplonyi', password='TSP123abc')
#cursor = conn.cursor()

def alg(p_c_raw, p_m_raw, pop_raw, gen_raw):

    # Importálás specificikus directoryból
    #r'D:\Users\Krisztian\Documents\CORVINUS\szakdoga\Python_TSP_app\Python_TSP_app\telepules_matrix.xls'
    #data1 = pd.read_excel ('telepules_matrix.xls', index_col=0)
    #print (data1)
    x0 = Kruskal.xFinal#kezdeti megoldás

    #print(x0)

    ###Parameterek###
    p_c = p_c_raw #crossover val
    p_m = p_m_raw #muation val
    #k = 3 #tournament selection(?)
    pop = pop_raw # pupolacio meret
    gen = gen_raw #generáció szám

    #total_tav_kezdo = OF.OF_cal(x0)

    Final_Best_in_Generation_X = []
    Final_Worst_in_Generation_X = []

    xFinal_ut = []
    xFinal = np.empty((0,len(x0)+2))

    Best_gyujto = np.empty((0,len(x0)+1))

    min_for_all_generations_MUT_1 = np.empty((0,len(x0)+1))
    min_for_all_generations_MUT_2 = np.empty((0,len(x0)+1))

    min_for_all_generations_MUT_1_1 = np.empty((0,len(x0)+2))
    min_for_all_generations_MUT_2_2 = np.empty((0,len(x0)+2))

    min_for_all_generations_MUT_1_1_1 = np.empty((0,len(x0)+2))
    min_for_all_generations_MUT_2_2_2 = np.empty((0,len(x0)+2))

    gen_counter = 1

    n_list = np.empty((0,len(x0)))

    #kezdeti populáciuó létrehozása
    for i in range(pop):
        rd.shuffle(x0) #véeletlen keverése a városoknak pop-szor
        n_list = np.vstack((n_list,x0)) #eltároljuk ezekeet egy listában



    for i in range(gen):
        new_pop = np.empty((0,len(x0))) #Uj generáció tárolása
        All_in_generation_x_1 = np.empty((0,len(x0)+1))
        All_in_generation_x_2 = np.empty((0,len(x0)+1))

        Min_in_generation_x_1 = []
        Min_in_generation_x_2 = []

        Best_a_x_genben = np.empty((0,len(x0)+1))
        
        #print("--> Generation: #", gen_counter)
        fam_counter = 1

        for j in range(int(pop/2)):
            #print("--> Family: #", fam_counter)

            #Tournament selection

            parents = np.empty((0,len(x0)+1))
            for i in range(2):
                battle_troops = []
                warrior_1_index = np.random.randint(0,len(n_list))
                warrior_2_index = np.random.randint(0,len(n_list))
                warrior_3_index = np.random.randint(0,len(n_list))

                while warrior_1_index==warrior_2_index:
                    warrior_1_index = np.random.randint(0,len(n_list))
                while warrior_2_index==warrior_3_index:
                    warrior_2_index = np.random.randint(0,len(n_list))
                while warrior_1_index==warrior_3_index:
                    warrior_3_index = np.random.randint(0,len(n_list))

                warrior_1=n_list[warrior_1_index]
                warrior_2=n_list[warrior_2_index]
                warrior_3=n_list[warrior_3_index]

                battle_troops=[warrior_1, warrior_2, warrior_3]

                OF_value_for_Wi= np.empty((0,len(x0)+1))
                OF_value_for_All_W = np.empty((0,len(x0)+1))
                
                ###OF###
                z = 1
                for warrior in battle_troops:
                    
                    warrior_tavok_temp=OF.OF_cal(warrior)
                    warrior = warrior[np.newaxis]
                    #print("OF_So_Far_W",z,": ",warrior_tavok_temp)
                    z=z+1
                    

                    OF_value_for_Wi = np.column_stack((warrior_tavok_temp, warrior))
                    OF_value_for_All_W = np.vstack((OF_value_for_All_W,OF_value_for_Wi))
                    
                Winner_i=np.empty((0,len(x0)+1))
                Winner_i=np.column_stack((OF_value_for_All_W[np.argmin(OF_value_for_All_W, axis=0)[0]]))
                parents=np.vstack((parents, Winner_i))
                #print("Winner: ", Winner_i)
                #print("Parents: ", parents)
            parent_1 = parents[0][1:]
            parent_2 = parents[1][1:]
            
            #Crossover

            child_1_lst = []
            child_2_lst = []
            child_1=np.empty((0,len(x0)))
            child_2=np.empty((0,len(x0)))

            #Where to crossover

            Rand_CO_1 = np.random.rand()

            if Rand_CO_1 < p_c:
                Cr_1 = np.random.randint(0,len(x0))
                Cr_2 = np.random.randint(0,len(x0))

                while Cr_1==Cr_2:
                    Cr_2 = np.random.randint(0,len(x0))

                if Cr_1<Cr_2:
                    

                    mid_seg_1 = parent_1[Cr_1:Cr_2+1]
                    mid_seg_2 = parent_2[Cr_1:Cr_2+1]

                    start_seg_1 = parent_1[:Cr_1]
                    end_seg_1 = parent_1[Cr_2+1:]

                    start_seg_2 = parent_2[:Cr_1]
                    end_seg_2 = parent_2[Cr_2+1:]

                    for i in range(len(x0)):
                        if i < Cr_1:
                            temp_1=start_seg_1[i]
                            while temp_1 in mid_seg_2:
                                temp_1=mid_seg_1[np.where(mid_seg_2==temp_1)][0]
                            temp_2=start_seg_2[i]
                            while temp_2 in mid_seg_1:
                                temp_2=mid_seg_2[np.where(mid_seg_1==temp_2)][0]
                            child_1_lst.append(temp_1)
                            child_2_lst.append(temp_2)
                        elif i>=Cr_1 and i<(Cr_2+1):
                            temp_1=mid_seg_2[i-Cr_1]
                            temp_2=mid_seg_1[i-Cr_1]
                            child_1_lst.append(temp_1)
                            child_2_lst.append(temp_2)
                        elif i>Cr_2:
                            temp_1=end_seg_1[(i-(Cr_2+1))]
                            while temp_1 in mid_seg_2:
                                temp_1=mid_seg_1[np.where(mid_seg_2==temp_1)][0]
                            temp_2=end_seg_2[(i-(Cr_2+1))]
                            while temp_2 in mid_seg_1:
                                temp_2=mid_seg_2[np.where(mid_seg_1==temp_2)][0]
                            child_1_lst.append(temp_1)
                            child_2_lst.append(temp_2)
                else:

                    mid_seg_1 = parent_1[Cr_2:Cr_1+1]
                    mid_seg_2 = parent_2[Cr_2:Cr_1+1]

                    start_seg_1 = parent_1[:Cr_2]
                    end_seg_1 = parent_1[Cr_1+1:]

                    start_seg_2 = parent_2[:Cr_2]
                    end_seg_2 = parent_2[Cr_1+1:]     
                    for i in range(len(x0)):
                        if i < Cr_2:
                            temp_1=start_seg_1[i]
                            while temp_1 in mid_seg_2:
                                temp_1=mid_seg_1[np.where(mid_seg_2==temp_1)][0]
                            temp_2=start_seg_2[i]
                            while temp_2 in mid_seg_1:
                                temp_2=mid_seg_2[np.where(mid_seg_1==temp_2)][0]
                            child_1_lst.append(temp_1)
                            child_2_lst.append(temp_2)
                        elif i>=Cr_2 and i<(Cr_1+1):
                            temp_1=mid_seg_2[i-Cr_2]
                            temp_2=mid_seg_1[i-Cr_2]
                            child_1_lst.append(temp_1)
                            child_2_lst.append(temp_2)
                        elif i>Cr_1:
                            temp_1=end_seg_1[(i-(Cr_1+1))]
                            while temp_1 in mid_seg_2:
                                temp_1=mid_seg_1[np.where(mid_seg_2==temp_1)][0]
                            temp_2=end_seg_2[(i-(Cr_1+1))]
                            while temp_2 in mid_seg_1:
                                temp_2=mid_seg_2[np.where(mid_seg_1==temp_2)][0]
                            child_1_lst.append(temp_1)
                            child_2_lst.append(temp_2)
                    
                #np.reshape(child_1, (0,len(x0)))
                #np.reshape(child_2, (0,len(x0)))
                
                child_1 = np.array(child_1_lst)
                child_2 = np.array(child_2_lst)

            else:
                child_1=parent_1
                child_2 = parent_2

            #print("\nCh_1: ", child_1)
            #print("Ch_2: ", child_2)
            
            #Mutation

            Mutated_child_1 = []

            for i in child_1:
                rand_mut_1 = np.random.rand() #prob to mutate

                if rand_mut_1<p_m:
                    mr_1 = np.random.randint(0,len(x0))
                    mr_2 = np.random.randint(0,len(x0))
                    
                    while mr_1==mr_2:
                        mr_2 = np.random.randint(0,len(x0))
                    
                    child_1[mr_1], child_1[mr_2] = child_1[mr_2], child_1[mr_1]

                    Mutated_child_1 = child_1
                else:
                    Mutated_child_1 = child_1

            Mutated_child_2 = []

            for i in child_2:
                rand_mut_2 = np.random.rand() #prob to mutate

                if rand_mut_2<p_m:
                    mr_1 = np.random.randint(0,len(x0))
                    mr_2 = np.random.randint(0,len(x0))
                    
                    while mr_1==mr_2:
                        mr_2 = np.random.randint(0,len(x0))
                    
                    child_2[mr_1], child_2[mr_2] = child_2[mr_2], child_2[mr_1]

                    Mutated_child_2 = child_2
                else:
                    Mutated_child_2 = child_2

            #OF value for mutated children
            total_MC_1=OF.OF_cal(Mutated_child_1)
            total_MC_2=OF.OF_cal(Mutated_child_2)

            #print("\nOF for MC1: ", total_MC_1, "\nOF for MC2: ", total_MC_2)
                                    
            All_in_generation_x_1_1_temp = Mutated_child_1[np.newaxis]                    
            All_in_generation_x_1_1 = np.column_stack((total_MC_1, All_in_generation_x_1_1_temp))

            All_in_generation_x_2_1_temp = Mutated_child_2[np.newaxis] 
            All_in_generation_x_2_1 = np.column_stack((total_MC_2, All_in_generation_x_2_1_temp))   

            All_in_generation_x_1 = np.vstack((All_in_generation_x_1, All_in_generation_x_1_1))
            All_in_generation_x_2 = np.vstack((All_in_generation_x_2, All_in_generation_x_2_1))
            
            Best_a_x_genben = np.vstack((All_in_generation_x_1,All_in_generation_x_2))

            new_pop = np.vstack((new_pop, Mutated_child_1, Mutated_child_2))

            t = 0
            r_1=[]

            for i in All_in_generation_x_1:
                if (All_in_generation_x_1[t,0])<=min(All_in_generation_x_1[:,0]):
                    r_1 = All_in_generation_x_1[t,:]
                t = t+1
            Min_in_generation_x_1 = r_1[np.newaxis]

            t = 0
            r_2=[]

            for i in All_in_generation_x_2:
                if (All_in_generation_x_2[t,0])<=min(All_in_generation_x_2[:,0]):
                    r_2 = All_in_generation_x_2[t,:]
                t = t+1
            Min_in_generation_x_2 = r_2[np.newaxis]

            fam_counter = fam_counter+1

        t=0
        r_final = []
        for i in Best_a_x_genben:
            if (Best_a_x_genben[t,0])<=min(Best_a_x_genben[:,0]):
                r_final= Best_a_x_genben[t,]
            t= t+1

        Final_Best_in_Generation_X = r_final[np.newaxis]
        Best_gyujto = np.vstack((Best_gyujto, Final_Best_in_Generation_X))
        
        t=0
        r_neg_final = []
        for i in Best_a_x_genben:
            if (Best_a_x_genben[t,0])>=max(Best_a_x_genben[:,0]):
                r_neg_final= Best_a_x_genben[t,]
            t= t+1

        Final_Worst_in_Generation_X = r_neg_final[np.newaxis]

        #Elitizmus

        Darwin_guy = Final_Best_in_Generation_X[:]
        Neg_Darwin_guy = Final_Worst_in_Generation_X[:]

        Darwin_guy = Darwin_guy[0:,1:].tolist()
        Neg_Darwin_guy = Neg_Darwin_guy[0:,1:].tolist()

        Best_1 = np.where((new_pop==Darwin_guy).all(axis=1))
        Worst_1 = np.where((new_pop==Neg_Darwin_guy).all(axis=1))

        new_pop[Worst_1] = Darwin_guy

        n_list = new_pop        

        min_for_all_generations_MUT_1 = np.vstack((min_for_all_generations_MUT_1, Min_in_generation_x_1))
        min_for_all_generations_MUT_2 = np.vstack((min_for_all_generations_MUT_2, Min_in_generation_x_2))

        min_for_all_generations_MUT_1_1 = np.insert(Min_in_generation_x_1, 0, gen_counter)
        min_for_all_generations_MUT_2_2 = np.insert(Min_in_generation_x_2, 0, gen_counter)

        min_for_all_generations_MUT_1_1_1 = np.vstack((min_for_all_generations_MUT_1_1_1, min_for_all_generations_MUT_1_1))
        min_for_all_generations_MUT_2_2_2 = np.vstack((min_for_all_generations_MUT_2_2_2, min_for_all_generations_MUT_2_2))

        gen_counter=gen_counter+1

    xFinal = np.vstack((min_for_all_generations_MUT_1_1_1,min_for_all_generations_MUT_2_2_2))
    xFinal_ut=np.column_stack((xFinal[np.argmin(xFinal, axis=0)[1]]))
    current_Date = datetime.now()
    formatted_date = current_Date.strftime('%Y-%m-%d')
    #SQLCommand="""INSERT INTO tsp.ga(run_time, OFV, p_c, p_m, pop, gen) VALUES(%s,%s,%s,%s,%s,%s)"""
    #Values = [formatted_date, float(xFinal_ut[0][1]), float(p_c), float(p_m), int(pop), int(gen)]
    #cursor.execute(SQLCommand, Values)
    #conn.commit()
    export = [] 
    export.append(formatted_date)
    export.append(float(xFinal_ut[0][1]))
    export.append(float(p_c))
    export.append(float(p_m))
    export.append(int(pop))
    export.append(int(gen))
    print("GA Siker!")
    return export
    #print("\nVégső megoldás: ", xFinal_ut)
    #print()
