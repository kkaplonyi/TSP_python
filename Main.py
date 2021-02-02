from datetime import datetime
import Tabu_kereses
import Szimulalt_hutes
import Genetikus
import pandas as pd
import numpy as np

xls = pd.ExcelFile('RAW_Parameters.xlsx')
ga_df = pd.read_excel(xls, 'ga', index_col=0)
sza_df = pd.read_excel(xls, 'sz_hutes', index_col=0)
tabu_df = pd.read_excel(xls, 'tabu', index_col=0)

ga_array = np.empty((0,6))
sza_array = np.empty((0,6))
tabu_array = np.empty((0,4))
harmonia_array = np.empty((0,4))

writer = pd.ExcelWriter('Results_sample.xlsx', engine='xlsxwriter')  

#TABU
for i in range(len(tabu_df)):
    start = datetime.now()
    for j in range(30):
        result_tabu = Tabu_kereses.alg(tabu_df.iat[i,0], tabu_df.iat[i,1])
        tabu_array = np.vstack((tabu_array,result_tabu))
    end = datetime.now()
    print("----------------> Futási szám: #",(i+1),". Futási idő:", (end-start), "<----------------")

tabu_export_df = pd.DataFrame(tabu_array, columns=['run_time', 'OFV', 'M', 'T_length'])
tabu_export_df.to_excel(writer, sheet_name='TABU')

#SZA
for i in range(150):
    start = datetime.now()
    for j in range(30):
        result_sza = Szimulalt_hutes.alg(sza_df.iat[i,0], sza_df.iat[i,1], sza_df.iat[i,2], sza_df.iat[i,3])
        sza_array = np.vstack((sza_array,result_sza))
    end = datetime.now()
    print("----------------> Futási szám: #",(i+1),". Futási idő:", (end-start), "<----------------")

sza_export_df = pd.DataFrame(sza_array, columns=['run_time', 'OFV', 'T0', 'M', 'N', 'alpha'])
sza_export_df.to_excel(writer, sheet_name='Szimulalt_hutes')

#GA
for i in range(len(ga_df)):
    start = datetime.now()
    for j in range(30):
        result_ga = Genetikus.alg(ga_df.iat[i,0], ga_df.iat[i,1], ga_df.iat[i,2], ga_df.iat[i,3])
        ga_array = np.vstack((ga_array,result_ga))
    end = datetime.now()
    print("----------------> Futási szám: #",(i+1),". Futási idő:", (end-start), "<----------------")

ga_export_df = pd.DataFrame(ga_array, columns=['run_time', 'OFV', 'p_c', 'p_m', 'pop', 'gen'])
ga_export_df.to_excel(writer, sheet_name='Genetic_algorithm')


writer.save()
print("Végig futott az összes!")

    
    
