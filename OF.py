import numpy as np
import pandas as pd

data1 = pd.read_excel('telepules_matrix.xls', index_col=0)
def OF_cal(x):
    tavolsagok=[] #a célfüggvény részértékei
    t=0
    for i in range(len(x)-1):
        x1=data1.loc[x[t],x[t+1]] # n és n+1 város
        x11 = data1.loc[x[-1],x[0]] #az utolsó és az első város   
        tavolsagok.append(x1)
        t=t+1


    tavolsagok.append(x11) #hozzáadjuk az utolsó városból a kezdő városba való költséget (kör bezárása)
    OF_value=sum(tavolsagok) #tavolságok összeadása
    return OF_value