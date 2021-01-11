import math
import pandas as pd
from matplotlib import pyplot as plt

m = float(input("Input start kapital: "))
y = int(input("Input hele år på kontoen: "))
o = float( input("Input opsarringsrente: "))

df = pd.DataFrame({"År":[],"Aktiespare":[], "Aktiespare_skat":[],"Anden_skat":[]})



def compund_interest_tax(money,year,increment,df):
    return_on_investment = money
    # diff = 0
    for i in range(0,year):
        tmp = return_on_investment + (return_on_investment / 100 * increment)
        return_on_investment = tmp
        if(i!=0):
            tax = df["Aktiespare_skat"].loc[i-1]+(tmp / 100 * 17)
        else:
            tax = tmp / 100 * 17
        tmpDf = pd.DataFrame({"År":[i+1],"Aktiespare":[return_on_investment],"Aktiespare_skat":[tax],"Anden_skat":[0]})
        df = df.append(tmpDf,ignore_index=True)
    return return_on_investment,df

def compund_interest_tax_2(money,year,increment,df):
    return_on_investment = money
    for i in range(0,year):
        return_on_investment = return_on_investment + (return_on_investment / 100 * increment)
        if(return_on_investment-money<=50000):
            tmp = return_on_investment /100 * 27
 #           tmp = return_on_investment - tmp
            df["Anden_skat"].iloc[i] = tmp
        else:
            tmp = return_on_investment /100 * 42
  #          tmp = return_on_investment - tmp
            df["Anden_skat"].iloc[i] = tmp
    if(return_on_investment-money<=50000):
        return_on_investment = return_on_investment - (return_on_investment/100*27)
    else:
        return_on_investment = return_on_investment - (return_on_investment/100*42)
        
    return return_on_investment,df


x,df = compund_interest_tax(m,y,o,df)
# print("====================\n\
# Betalts aktiesparekonto:")
# print(x)
y,df = compund_interest_tax_2(m,y,o,df)
# print("====================\n\
# Indtjening på andet aktiedepot:")
# print(y)
# print("====================")

z = df["År"]
p = df["Aktiespare_skat"]
h = df["Anden_skat"]
plt.plot(z,p,'b-',label = 'Aktiesparekonto betalt skat')
plt.plot(z,h,'r-',label = 'Andet depot skat')
plt.legend(loc = 'best')
plt.show()