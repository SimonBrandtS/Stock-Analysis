import math
import pandas as pd
from matplotlib import pyplot as plt

running = True


def continue_script():
    to_do = input("Try something else? \n\
yes/no: ")
    tmp = True
    if('no' == to_do):
        tmp = False
    elif('yes' == to_do):
        print("====================")
    else:
        print("Invalid input.")
        continue_script()
    input("Press Enter to continue...")
    return tmp


def compund_interest_tax(money, year, increment, df):
    return_on_investment = money
    # diff = 0
    for i in range(0, year):
        tmp = return_on_investment + (return_on_investment / 100 * increment)
        return_on_investment = tmp
        if(i != 0):
            tax = df["Aktiespare_skat"].loc[i-1]+(tmp / 100 * 17)
        else:
            tax = tmp / 100 * 17
        tmpDf = pd.DataFrame(
            {"År": [i+1], "Aktiespare": [return_on_investment], "Aktiespare_skat": [tax], "Anden_skat": [0]})
        df = df.append(tmpDf, ignore_index=True)
    return return_on_investment, df


def compund_interest_tax_2(money, year, increment, df):
    return_on_investment = money
    for i in range(0, year):
        return_on_investment = return_on_investment + \
            (return_on_investment / 100 * increment)
        if(return_on_investment-money <= 50000):
            tmp = return_on_investment / 100 * 27
        #           tmp = return_on_investment - tmp
            df["Anden_skat"].iloc[i] = tmp
        else:
            tmp = return_on_investment / 100 * 42
        #          tmp = return_on_investment - tmp
            df["Anden_skat"].iloc[i] = tmp
    if(return_on_investment-money <= 50000):
        return_on_investment = return_on_investment - \
            (return_on_investment/100*27)
    else:
        return_on_investment = return_on_investment - \
            (return_on_investment/100*42)

    return return_on_investment, df


while running:
    to_do = input("What do you wish to do?\n\
Calculate tax based on manual input: 'man'\n\
For projected tax based on stock: 'auto'    \n\
To end program: 'stop'\n\
Input: ")

    if('man' == to_do):
        print("====================")
        m = float(input("Input starting capital on account: "))
        y = int(input("Input expected years on account: "))
        o = float(input("Input projected growth rate: "))

        df = pd.DataFrame({"År": [], "Aktiespare": [],
                           "Aktiespare_skat": [], "Anden_skat": []})

        x, df = compund_interest_tax(m, y, o, df)

        y, df = compund_interest_tax_2(m, y, o, df)

        z = df["År"]
        p = df["Aktiespare_skat"]
        h = df["Anden_skat"]
        plt.plot(z, p, 'b-', label='Aktiesparekonto paid tax')
        plt.plot(z, h, 'r-', label='Other depot tax')
        plt.legend(loc='best')
        plt.show()
        print("====================")
        to_do_two = continue_script()
        if(False == to_do_two):
            print("====================")
            print("Goodbye :-)")
            running = to_do_two
        

    elif('auto' == to_do):
        print("====================")
        print("This feature is still being developed! Hold tight")
        print("====================")
        input("Press Enter to continue...")
    elif('stop' == to_do):
        running = False
        print("====================")
        print("Goodbye :-)")
    else:
        print("====================")
        print("Unkwown input, please try again")
        print("====================")
        input("Press Enter to continue...")