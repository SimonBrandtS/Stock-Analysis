import math
import pandas as pd
from matplotlib import pyplot as plt
import yfinance as yf
import datetime
import pandas_market_calendars as mcal
import re
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


def is_gap_year(year):
    x = 0
    if(year > 2020):
        x = year % 2020
    else:
        x = 2020 % year
    if(x == 4):
        return True
    else:
        return False


def Average(lst):
    return sum(lst) / len(lst)


def calculate_average_growth(hist):
    total_date = datetime.datetime.today()
    yearly_avg = []
    cal = mcal.get_calendar('NYSE')

    first_day = hist.iloc[0].name
    first_close = hist.iloc[0].Close
    first_wekday = first_day.weekday()

    year = first_day.year
    day = first_day.day
    month = first_day.month

    next_year = year + 1
    schecdule = cal.schedule(
        start_date=f'{year}-{month}-{day}', end_date=f'{next_year}-{month}-{day}')
    last_day = schecdule.iloc[-1]

    final_day = last_day[1].day
    final_year = last_day[1].year
    final_month = last_day[1].month

    for i, row in hist.iterrows():
        if(i.year == final_year and i.day == final_day and i.month == final_month):
            year = final_year
            day = final_day
            month = final_month
            next_year = year + 1
            schecdule = cal.schedule(
                start_date=f'{year}-{month}-{day}', end_date=f'{next_year}-{month}-{day}')
            iter_close = row.Close
            diff = (iter_close-first_close)/first_close*100
            yearly_avg.append(diff)
            last_day = schecdule.iloc[-1]

            final_day = last_day[1].day
            final_year = last_day[1].year
            final_month = last_day[1].month

            first_close = iter_close

    return(Average(yearly_avg))


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
            df["Anden_skat"].iloc[i] = tmp
        else:
            tmp = return_on_investment / 100 * 42
            df["Anden_skat"].iloc[i] = tmp
    if(return_on_investment-money <= 50000):
        return_on_investment = return_on_investment - \
            (return_on_investment/100*27)
    else:
        return_on_investment = return_on_investment - \
            (return_on_investment/100*42)

    return return_on_investment, df



def plotTax(df):
    z = df["År"]
    p = df["Aktiespare_skat"]
    h = df["Anden_skat"]
    plt.plot(z, p, 'b-', label='Aktiesparekonto paid tax')
    plt.plot(z, h, 'r-', label='Other depot tax')
    plt.legend(loc='best')
    plt.show()



def main(running):
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

            plotTax(df)

            print("====================")
            to_do_two = continue_script()
            if(False == to_do_two):
                print("====================")
                print("Goodbye :-)")
                running = to_do_two

        elif('auto' == to_do):
            tcr = input("Please enter Ticker: ")
            stock = yf.Ticker(tcr)
            period = input(
                "Please input historical period as number + period type e.g. '3y' for 3 days (default is 5 years i.e. 5y): ")
            test_string = re.findall('^[0-9][y]$',period)
            if('' == period):
                hist = stock.history(period="5y")
                o = calculate_average_growth(hist)
            elif(len(test_string)!=0):
                print("todo: develop")
                hist = stock.history(period = period)
                o = calculate_average_growth(hist)
            else:
                print("====================")
                print("Sorry, for now the input must be in years (i.e. '5y'")
                to_do_two = continue_script()
                if(False == to_do_two):
                    print("====================")
                    print("Goodbye :-)")
                    running = to_do_two
                    break
                else:
                    main(running)

            m = float(input("Input starting capital on account: "))
            y = int(input("Input expected years on account: "))

            df = pd.DataFrame({"År": [], "Aktiespare": [],
                            "Aktiespare_skat": [], "Anden_skat": []})

            x, df = compund_interest_tax(m, y, o, df)

            y, df = compund_interest_tax_2(m, y, o, df)
            

            plotTax(df)
            print("====================")
            to_do_two = continue_script()
            if(False == to_do_two):
                    print("====================")
                    print("Goodbye :-)")
                    running = to_do_two
        elif('stop' == to_do):
            running = False
            print("====================")
            print("Goodbye :-)")
        else:
            print("====================")
            print("Unkwown input, please try again")
            print("====================")
            input("Press Enter to continue...")
main(running)